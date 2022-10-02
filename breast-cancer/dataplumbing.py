#########################################################################################
# Author: Jared L. Ostmeyer
# Date Started: 2021-11-16
# Environment: Python3
# Purpose: Utilities for loading immune receptor sequences
##########################################################################################

##########################################################################################
# Libraries
##########################################################################################

import csv
import zipfile
import io
from itertools import combinations

##########################################################################################
# Utilities
##########################################################################################

def load_cdr3s(path_tsv, min_length=4, max_length=32, version='v2'):
  receptors = {}
  with open(path_tsv, 'r') as stream:
    reader = csv.DictReader(stream, delimiter='\t')
    for row in reader:
      if version == 'v2':
        cdr3 = row['aminoAcid']
#        quantity = float(row['frequencyCount (%)'])
        quantity = float(row['count (templates/reads)'])
        status = row['sequenceStatus']
      elif version == 'v3':
        cdr3 = row['amino_acid']
#        quantity = float(row['frequency'])
        quantity = float(row['templates'])
        status = row['frame_type']
      else:
        print('ERROR: Unsupported version')
        exit()
      if 'In' in status and min_length <= len(cdr3) and len(cdr3) <= max_length and quantity > 0.0 and 'X' not in cdr3:
        if cdr3 not in receptors:
          receptors[cdr3] = quantity
        else:
          receptors[cdr3] += quantity
  return receptors

def trim_cdr3s(receptors, trim_front=0, trim_rear=0):
  cdr3s = {}
  for cdr3, quantity in receptors.items():
    cdr3_trim = cdr3[trim_front:]
    if trim_rear > 0:
      cdr3_trim = cdr3_trim[:-trim_rear]
    if len(cdr3_trim) > 0:
      if cdr3_trim not in cdr3s:
        cdr3s[cdr3_trim] = quantity
      else:
        cdr3s[cdr3_trim] += quantity
  return cdr3s

def cdr3s_to_kmers(cdr3s, kmer_size):
  kmers = {}
  for cdr3, quantity in cdr3s.items():
    if len(cdr3) >= kmer_size:
      for i in range(len(cdr3)-kmer_size+1):
        kmer = cdr3[i:i+kmer_size]
        if kmer not in kmers:
          kmers[kmer] = quantity
        else:
          kmers[kmer] += quantity
  return kmers

def cdr3s_to_motifs(cdr3s, window_size, motif_size):
  templates = []
  for template in list(combinations(range(window_size), motif_size)):
    if template[0] == 0:
      templates.append(template)
  motifs = {}
  for cdr3, quantity in cdr3s.items():
    if len(cdr3) >= motif_size:
      for i in range(len(cdr3)-motif_size+1):
        window = cdr3[i:i+window_size]
        for template in templates:
          if template[-1] < len(window):
            motif = ''
            for i in template:
              motif += window[i]
            if motif not in motifs:
              motifs[motif] = quantity
            else:
              motifs[motif] += quantity
  return motifs

def flatten_sample(sequences):
  return { sequence: 1.0 for sequence in sequences.keys() }

def normalize_sample(sequences):
  total = 0.0
  for quantity in sorted(sequences.values()):
    total += quantity
  sequences_ = {}
  for sequence, quantity in sequences.items():
    sequences_[sequence] = quantity/total
  return sequences_

def merge_samples(samples):
  sequences = {}
  for sample in samples:
    for sequence, quantity in sample.items():
      if sequence not in sequences:
        sequences[sequence] = quantity/float(len(samples))
      else:
        sequences[sequence] += quantity/float(len(samples))
  return sequences

def debug_insert_sequence(receptors, sequence, count):
  if sequence not in receptors:
    receptors[sequence] = count
  else:
    receptors[sequence] += count
  return receptors
