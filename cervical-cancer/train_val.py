#!/usr/bin/env python3
##########################################################################################
# Author: Jared L. Ostmeyer
# Date Started: 2021-11-16
# Purpose: Train and validate a classifier for immune repertoires
##########################################################################################

##########################################################################################
# Libraries
##########################################################################################

import argparse
import csv
import glob
import dataplumbing as dp
import dataset as ds
import numpy as np
import torch

##########################################################################################
# Arguments
##########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--holdouts', help='Holdout samples', type=str, nargs='+', required=True)
parser.add_argument('--restart', help='Basename for restart files', type=str, default=None)
parser.add_argument('--output', help='Basename for output files', type=str, required=True)
parser.add_argument('--seed', help='Seed value for randomly initializing fits', type=int, default=1)
parser.add_argument('--device', help='Examples are cuda:0 or cpu', type=str, default='cuda:0')
parser.add_argument('--num_fits', help='Number of fits to the training data', type=int, default=2**17)
args = parser.parse_args()

##########################################################################################
# Assemble sequences
##########################################################################################

# Settings
#
trim_front = 3
trim_rear = 3

window_size = 4
motif_size = 3

# To hold sequences from each subject
#
cases = {}
controls = {}

# Labels
#
samples = {
  '2-30_DNA': 'regress',
  '2_31': 'regress',
  '3-11_DNA': 'progress',
  '112015051_3_32': 'regress',
  '112015051_3_38': 'regress',
  '112015051_3_39': 'regress',
  '3-4_DNA': 'progress',
  '112015051_3_40': 'progress',
  '3-6_DNA': 'regress',
  '4-1_DNA': 'regress',
  '4-11_DNA': 'regress',
  '4-13_DNA': 'regress',
  '4-2_DNA': 'regress',
  '4-22_DNA': 'regress',
  '112015051_4_33': 'regress',
  '112015051_4_38': 'progress',
  '5-15_DNA': 'regress',
  '5-19_DNA': 'same',
  '5-27A_DNA': 'regress',
  '112015051_5_31': 'regress',
  '112015051_5_33': 'regress',
  '112015051_5_35': 'regress',
  '112015051_5_39': 'same',
  '5-6_DNA': 'regress'
}

# Load immune repertoires
#
for sample, label in samples.items():
  path = 'dataset/'+sample+'.tsv'
  cdr3s = dp.load_cdr3s(path, min_length=kmer_size+trim_front+trim_rear, max_length=32)
  cdr3s = dp.trim_cdr3s(cdr3s, trim_front=trim_front, trim_rear=trim_rear)
  kmers = dp.cdr3s_to_kmers(cdr3s, kmer_size)
  kmers = dp.normalize_sample(kmers)
  if 'regress' in cases:
    cases[sample] = kmers
  else:
    controls[sample] = kmers

##########################################################################################
# Assemble datasets
##########################################################################################

# Load embeddings
#
aminoacids_dict = ds.load_aminoacid_embedding_dict('../aminoacid-representation/atchley_factors_normalized.csv')

# Convert to numeric representations
#
samples = ds.assemble_samples(cases, controls, aminoacids_dict)

# Split into a training and validation cohort
#
samples_train, samples_val = ds.split_samples(samples, args.holdouts)

# Weight samples
#
samples_train = ds.weight_samples(samples_train)
samples_val = ds.weight_samples(samples_val)

# Normalize features
#
samples_train, samples_val = ds.normalize_samples(samples_train, samples_val)

##########################################################################################
# Assemble tensors
##########################################################################################

# Settings
#
device = torch.device(args.device)

# Convert numpy arrays to pytorch tensors
#
for sample in samples_train:
  sample['features'] = torch.from_numpy(sample['features']).to(device)
  sample['label'] = torch.tensor(sample['label']).to(device)
  sample['weight'] = torch.tensor(sample['weight']).to(device)

# Convert numpy arrays to pytorch tensors
#
for sample in samples_val:
  sample['features'] = torch.from_numpy(sample['features']).to(device)
  sample['label'] = torch.tensor(sample['label']).to(device)
  sample['weight'] = torch.tensor(sample['weight']).to(device)

##########################################################################################
# Model
##########################################################################################

# Settings
#
num_features = samples_train[0]['features'].shape[1]
num_fits = args.num_fits

torch.manual_seed(args.seed)

# Function for initializing the weights of the model
#
def init_weights():
  return torch.cat(
    [
      0.5**0.5*torch.rand([ num_features-1, num_fits ])/(num_features-1.0)**0.5,  # Weights for the Atchley factors
      0.5**0.5*torch.rand([ 1, num_fits ])/(1.0)**0.5,  # Weight for the abundance term
    ],
    0
  )

# Class defining the model
#
class MaxSnippetModel(torch.nn.Module):
  def __init__(self):
    super(MaxSnippetModel, self).__init__()
    self.linear = torch.nn.Linear(num_features, num_fits)
    with torch.no_grad():
      self.linear.weights = init_weights()  # Initialize the weights
  def forward(self, x):
    ls = self.linear(x)
    ms, _ = torch.max(ls, axis=0)
    return ms

# Instantiation of the model
#
msm = MaxSnippetModel()

# Turn on GPU acceleration
#
msm.to(device)

##########################################################################################
# Metrics and optimization
##########################################################################################

# Settings
#
learning_rate = 0.01

# Optimizer
#
optimizer = torch.optim.Adam(msm.parameters(), lr=learning_rate)  # Adam is based on gradient descent but better

# Metrics
#
loss = torch.nn.BCEWithLogitsLoss(reduction='none')  # The loss function is calculated seperately for each fit by setting reduction to none

def accuracy(ls_block, ys_block):  # The binary accuracy is calculated seperate for each fit
  a = torch.nn.Sigmoid()
  ps_block = a(ls_block)
  cs_block = (torch.round(ps_block) == torch.round(ys_block)).to(ys_block.dtype)
  return cs_block

##########################################################################################
# Fit and evaluate model
##########################################################################################

# Settings
#
num_epochs = 2048

# Restore saved models
#
if args.restart is not None:
  msm = torch.load(args.output+'_model.p')

# Each iteration represents one batch
#
for epoch in range(0, num_epochs):

  # Reset the gradients
  #
  optimizer.zero_grad()

  es_train = 0.0  # Cross-entropy error
  as_train = 0.0  # Accuracy

  for sample in samples_train:

    xs_block = sample['features']
    ys_block = torch.tile(sample['label'], [ num_fits ])
    w_block = sample['weight']

    ls_block = msm(xs_block)
    sample['predictions'] = torch.sigmoid(ls_block)

    es_block = w_block*loss(ls_block, ys_block)  # The loss function is calculated seperately for each fit
    as_block = w_block*accuracy(ls_block, ys_block)  # The binary accuracy is calculated seperate for each fit

    es_train += es_block
    as_train += as_block

    e_block = torch.sum(es_block)
    e_block.backward()

  i_bestfit = torch.argmin(es_train)  # Very important index selects the best fit to the training data

  es_val = 0.0
  as_val = 0.0

  with torch.no_grad():

    for sample in samples_val:

      xs_block = sample['features']
      ys_block = torch.tile(sample['label'], [ num_fits ])
      w_block = sample['weight']

      ls_block = msm(xs_block)
      sample['predictions'] = torch.sigmoid(ls_block)

      es_block = w_block*loss(ls_block, ys_block)  # The loss function is calculated seperately for each fit
      as_block = w_block*accuracy(ls_block, ys_block)  # The binary accuracy is calculated seperate for each fit

      es_val += es_block
      as_val += as_block

  # Print report
  #
  print(
    'Epoch:', epoch,
    'Accuracy (train):', round(100.0*float(as_train[i_bestfit]), 2), '%',
    'Accuracy (val):', round(100.0*float(as_val[i_bestfit]), 2), '%',
    flush=True
  )

  # Save parameters and results from the best fit to the training data
  #
  if epoch%32 == 0:
    ws = msm.linear.weights.detach().numpy()
    bs = msm.linear.bias.detach().numpy()
    np.savetxt(args.output+'_'+str(epoch)+'_ws.csv', ws[:,i_bestfit])
    np.savetxt(args.output+'_'+str(epoch)+'_b.csv', bs[[i_bestfit]])
    with open(args.output+'_'+str(epoch)+'_ms_train.csv', 'w') as stream:
      print('Cross Entropy (bits)', 'Accuracy (%)', sep=',', file=stream)
      print(float(es_train[i_bestfit])/np.log(2.0), 100.0*float(as_train[i_bestfit]), sep=',', file=stream)
    with open(args.output+'_'+str(epoch)+'_ms_val.csv', 'w') as stream:
      print('Cross Entropy (bits)', 'Accuracy (%)', sep=',', file=stream)
      print(float(es_val[i_bestfit])/np.log(2.0), 100.0*float(as_val[i_bestfit]), sep=',', file=stream)
    with open(args.output+'_'+str(epoch)+'_ps_train.csv', 'w') as stream:
      print('Subject', 'Label', 'Weight', 'Prediction', sep=',', file=stream)
      for sample in samples_train:
        print(sample['subject'], float(sample['label']), float(sample['weight']), float(sample['predictions'][i_bestfit]), sep=',', file=stream)
    with open(args.output+'_'+str(epoch)+'_ps_val.csv', 'w') as stream:
      print('Subject', 'Label', 'Weight', 'Prediction', sep=',', file=stream)
      for sample in samples_val:
        print(sample['subject'], float(sample['label']), float(sample['weight']), float(sample['predictions'][i_bestfit]), sep=',', file=stream)

  optimizer.step()

torch.save(msm, args.output+'_model.p')
