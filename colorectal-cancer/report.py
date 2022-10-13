#!/usr/bin/env python3
##########################################################################################
# Author: Jared L. Ostmeyer
# Date Started: 2018-02-05
# Purpose: Print results of the holdout cross-validation
##########################################################################################

##########################################################################################
# Libraries
##########################################################################################

import glob
import csv
from scipy.special import xlogy
import numpy as np

##########################################################################################
# Load data
##########################################################################################

steps_train = {}
for path in glob.glob('bin/*_ps_train.csv'):
  filename = path.split('/')[-1].split('.')[0]
  index, step, _, _ = filename.split('_')
  index_ = int(index)
  step_ = int(step)
  cost = 0.0
  accuracy = 0.0
  with open(path, 'r') as stream:
    reader = csv.DictReader(stream)
    for row in reader:
      subject = row['Subject']
      label = float(row['Label'])
      weight = float(row['Weight'])
      prediction = float(row['Prediction'])
      cost += weight*(-xlogy(label, prediction)-xlogy(1.0-label, 1.0-prediction))/np.log(2.0)
      accuracy += weight*100.0*np.equal(np.round(label), np.round(prediction)).astype(np.float64)
  if step_ not in steps_train:
    steps_train[step_] = {}
  if label not in steps_train[step_]:
    steps_train[step_][label] = {}
  steps_train[step_][label][index_] = { 'accuracy': accuracy, 'cost': cost }

steps_val = {}
for path in glob.glob('bin/*_ps_val.csv'):
  filename = path.split('/')[-1].split('.')[0]
  index, step, _, _ = filename.split('_')
  index_ = int(index)
  step_ = int(step)
  cost = 0.0
  accuracy = 0.0
  with open(path, 'r') as stream:
    reader = csv.DictReader(stream)
    for row in reader:
      subject = row['Subject']
      label = float(row['Label'])
      weight = float(row['Weight'])
      prediction = float(row['Prediction'])
      cost += weight*(-xlogy(label, prediction)-xlogy(1.0-label, 1.0-prediction))/np.log(2.0)
      accuracy += weight*100.0*np.equal(np.round(label), np.round(prediction)).astype(np.float64)
  if step_ not in steps_val:
    steps_val[step_] = {}
  if label not in steps_val[step_]:
    steps_val[step_][label] = {}
  steps_val[step_][label][index_] = { 'accuracy': accuracy, 'cost': cost }

##########################################################################################
# Results
##########################################################################################

print(
  'Step',
  ','.join([ 'Train_Accuracy_'+str(int(label)) for label in sorted(steps_train[32].keys()) ]),
  'Train_Accuracy',
  'Train_Cost',
  ','.join([ 'Val_Accuracy_'+str(int(label)) for label in sorted(steps_val[32].keys()) ]),
  'Val_Accuracy',
  'Val_Cost',
  sep=','
)

for step in sorted(steps_train.keys()):

  labels = steps_train[step]
  costs_train = []
  accuracies_train = []
  for label in sorted(labels.keys()):
    cost_total = 0.0
    accuracy_total = 0.0
    count_total = 0.0
    indices = labels[label]
    for index, metrics in indices.items():
      cost_total += metrics['cost']
      accuracy_total += metrics['accuracy']
      count_total += 1.0
    costs_train.append(cost_total/count_total)
    accuracies_train.append(accuracy_total/count_total)

  labels = steps_val[step]
  costs_val = []
  accuracies_val = []
  for label in sorted(labels.keys()):
    cost_total = 0.0
    accuracy_total = 0.0
    count_total = 0.0
    indices = labels[label]
    for index, metrics in indices.items():
      cost_total += metrics['cost']
      accuracy_total += metrics['accuracy']
      count_total += 1.0
    costs_val.append(cost_total/count_total)
    accuracies_val.append(accuracy_total/count_total)

  print(
    step,
    ','.join([ str(accuracy) for accuracy in accuracies_train ]),
    np.mean(accuracies_train),
    np.mean(costs_train),
    ','.join([ str(accuracy) for accuracy in accuracies_val ]),
    np.mean(accuracies_val),
    np.mean(costs_val),
    sep=','
  )
