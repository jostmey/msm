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
import numpy as np

##########################################################################################
# Data
##########################################################################################

holdouts = {}

for path in glob.glob('../bin/*.out'):
  holdout = path.split('/')[-1].split('_')[2]
  if holdout not in holdouts:
    holdouts[holdout] = {
      'Train': { 'Costs': [], 'Accuracies': [] },
      'Val': { 'Costs': [], 'Accuracies': [] }
    }
  with open(path, 'r') as stream:
    for line in stream:
      rows = line.split('\t')
      iteration = int(rows[0])
      cost_train = np.float64(rows[6])
      accuracy_train = np.float64(rows[7])
      cost_val = np.float64(rows[8])
      accuracy_val = np.float64(rows[9])
      if iteration >= len(holdouts[holdout]['Train']['Costs']):
        holdouts[holdout]['Train']['Costs'].append(cost_train)
        holdouts[holdout]['Train']['Accuracies'].append(accuracy_train)
        holdouts[holdout]['Val']['Costs'].append(cost_val)
        holdouts[holdout]['Val']['Accuracies'].append(accuracy_val)
      elif cost_train < holdouts[holdout]['Train']['Costs'][iteration]:
        holdouts[holdout]['Train']['Costs'][iteration] = cost_train
        holdouts[holdout]['Train']['Accuracies'][iteration] = accuracy_train
        holdouts[holdout]['Val']['Costs'][iteration] = cost_val
        holdouts[holdout]['Val']['Accuracies'][iteration] = accuracy_val

##########################################################################################
# Results
##########################################################################################

iteration = 0
while True:
  number = np.float64(0.0)
  cost_train = np.float64(0.0)
  accuracy_train = np.float64(0.0)
  cost_val = np.float64(0.0)
  accuracy_val = np.float64(0.0)
  for data in holdouts.values():
    if iteration < len(data['Train']['Costs']):
      number += np.float64(1.0)
      cost_train += data['Train']['Costs'][iteration]
      accuracy_train += data['Train']['Accuracies'][iteration]
      cost_val += data['Val']['Costs'][iteration]
      accuracy_val += data['Val']['Accuracies'][iteration]
  if number <= 0.5:
    break
  cost_train /= number
  accuracy_train /= number
  cost_val /= number
  accuracy_val /= number
  print(
    'Iteration:', iteration,
    'Number:', int(number),
    'Cost (Train):', '%4.3f'%cost_train,
    'Accuracy (Train):', '%4.3f'%accuracy_train,
    'Cost (Val):', '%4.3f'%cost_val,
    'Accuracy (Val):', '%4.3f'%accuracy_val
  )
  iteration += 1


