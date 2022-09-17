
import csv
import glob

cases = {}
controls = {}

for path in glob.glob('dataset/*.tsv'):
  sample = path.split('/')[-1].split('.')[0]
  label = sample[-1]
  if label == 'M' or label == 'N':
    if label == 'M':
      cases[sample] = {}
    else:
      controls[sample] = {}

print(cases, controls)
