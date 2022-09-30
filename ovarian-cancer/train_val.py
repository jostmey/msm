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
import os
import csv
import glob
import dataplumbing as dp
import dataset as ds
import torch

##########################################################################################
# Arguments
##########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--holdouts', help='Holdout samples', type=str, nargs='+', required=True)
parser.add_argument('--restart', help='Basename for restart files', type=str, default=None)
parser.add_argument('--output', help='Basename for output files', type=str, required=True)
parser.add_argument('--seed', help='Seed value for randomly initializing fits', type=int, default=1)
parser.add_argument('--gpu', help='GPU ID', type=int, default=0)
args = parser.parse_args()

##########################################################################################
# Environment
##########################################################################################

os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)

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

# Load immune repertoires
#
for path in glob.glob('dataset/*.tsv'):
  sample = path.split('/')[-1].split('.')[0]
  label = sample[-1]
  if label == 'M' or label == 'N':
    cdr3s = dp.load_cdr3s(path, min_length=motif_size+trim_front+trim_rear, max_length=32)
    cdr3s = dp.trim_cdr3s(cdr3s, trim_front=trim_front, trim_rear=trim_rear)
    motifs = dp.cdr3s_to_motifs(cdr3s, window_size, motif_size)
    motifs = dp.normalize_sample(motifs)
    if label == 'M':
      cases[sample] = motifs
    else:
      controls[sample] = motifs

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

# Convert numpy arrays to pytorch tensors
#
for sample in samples_train:
  sample['features'] = torch.from_numpy(sample['features']).cuda()
  sample['label'] = torch.tensor(sample['label']).cuda()
  sample['weight'] = torch.tensor(sample['weight']).cuda()

# Convert numpy arrays to pytorch tensors
#
for sample in samples_val:
  sample['features'] = torch.from_numpy(sample['features']).cuda()
  sample['label'] = torch.tensor(sample['label']).cuda()
  sample['weight'] = torch.tensor(sample['weight']).cuda()

##########################################################################################
# Model
##########################################################################################

# Settings
#
num_features = samples_train[0]['features'].shape[1]
num_fits = 2**17

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
msm.cuda()

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

    es_block = w_block*loss(ls_block, ys_block)  # The loss function is calculated seperately for each fit
    as_block = w_block*accuracy(ls_block, ys_block)  # The binary accuracy is calculated seperate for each fit

    es_train += es_block
    as_train += as_block

    e_block = torch.sum(es_block)
    e_block.backward()

  i_bestfit = torch.argmin(es_train)

  es_val = 0.0
  as_val = 0.0

  with torch.no_grad():

    for sample in samples_val:

      xs_block = sample['features']
      ys_block = torch.tile(sample['label'], [ num_fits ])
      w_block = sample['weight']

      ls_block = msm(xs_block)

      es_block = w_block*loss(ls_block, ys_block)  # The loss function is calculated seperately for each fit
      as_block = w_block*accuracy(ls_block, ys_block)  # The binary accuracy is calculated seperate for each fit

      es_val += es_block
      as_val += as_block

  # Print report
  #
  ln2 = 0.69314718056
  print(
    epoch,
    float(torch.mean(es_train))/ln2, 100.0*float(torch.mean(as_train)),
    float(torch.mean(es_val))/ln2, 100.0*float(torch.mean(as_val)),
    int(i_bestfit),
    float(es_train[i_bestfit])/ln2, 100.0*float(as_train[i_bestfit]),
    float(es_val[i_bestfit])/ln2, 100.0*float(as_val[i_bestfit]),
    sep='\t', flush=True
  )

  optimizer.step()

torch.save(msm, args.output+'_model.p')

