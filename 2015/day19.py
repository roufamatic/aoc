import os
from parse import parse
from copy import deepcopy
from collections import defaultdict
from frozendict import frozendict
from frozenlist import FrozenList
from functools import cache, reduce
import heapq
import math
import json
from itertools import combinations
from collections import deque
import Levenshtein
import re

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Run(path):
  parts = ReadFile(path).split('\n\n')
  molecule = parts[1]
  transforms = []
  for l in parts[0].splitlines():
    transforms.append(tuple(l.split(' => ')))
  rez = set()
  for t in transforms:
    for ix in range(len(molecule)):
      if molecule[ix:].startswith(t[0]):
        rez.add(molecule[:ix] + t[1] + molecule[ix + len(t[0]):])
  return len(rez)

def Run2(path):
  parts = ReadFile(path).split('\n\n')
  molecule = re.findall('[A-Z][a-z]?', parts[1])
  
  # all general strategies that I can think of fail for this due to the input size,
  # so I need to inspect the input for patterns.
  # In the input file:
  # * all transitions are of the form m0 -> m1m2
  # * m1 is always a single element
  # * m2 could be a single element OR it could be a compound
  # * compound looks like RnX(YX)+Ar where X is any element
  # steps to reduce it...
  # * start at count = -1 (the first element is skipped because we end with a single element)
  # * add one for each element
  # * if you reach an Ar: still add one but skip the next element
  # * if you reach a Y: skip it AND skip the next element
  # * if you reach an Rn: skip it
  # * otherwise: count it

  count = -1
  ix = 0
  while ix < len(molecule):
    a = molecule[ix]
    if a == 'Rn':
      count += 1 # the Rn marks the beginning of something to merge so it still is counted.
      ix += 2    # ... but we skip the next element since it's the first thing inside.
    elif a == 'Y':
      ix += 2    # Y is not counted, and the next atom is also not counted as a new first thing.
    elif a == 'Ar': # Ar is the end of the Rn so it is not counted.
      ix += 1
    else:
      count += 1
      ix += 1
  
  return count


if __name__ == '__main__':
  assert Run('input/19t.txt') == 7, Run('input/19t.txt')
  print(Run('input/19.txt'))
  #assert Run2('input/19t.txt') == 6, Run2('input/19t.txt') # solution doesn't generalize to the test input!
  print(Run2('input/19.txt'))
