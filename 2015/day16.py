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
from itertools import permutations

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output


def Run(path):
  known = {
      ('children', 3),
      ('cats', 7),
      ('samoyeds', 2),
      ('pomeranians', 3),
      ('akitas', 0),
      ('vizslas', 0),
      ('goldfish', 5),
      ('trees', 3),
      ('cars', 2),
      ('perfumes', 1),
  }
  for l in ReadFile(path).splitlines():
    v = parse('Sue {:d}: {}: {:d}, {}: {:d}, {}: {:d}', l)
    vv = { (v[1], v[2]), (v[3], v[4]), (v[5], v[6])}
    if vv & known == vv:
      print(v[0])
      break

  k2 = {v[0]:v[1] for v in known}
  for l in ReadFile(path).splitlines():
    v = parse('Sue {:d}: {}: {:d}, {}: {:d}, {}: {:d}', l)
    vv = { (v[1], v[2]), (v[3], v[4]), (v[5], v[6])}
    found = True
    for vvv in vv:
      if vvv[0] in ['cats','trees']:
        if k2[vvv[0]] >= vvv[1]: 
          found = False
          break
      elif vvv[0] in ['pomeranians', 'goldfish']:
        if k2[vvv[0]] <= vvv[1]: 
          found = False
          break
      else:
        if vvv not in known: 
          found = False
          break
    if found:    
      print(v[0])
      return


if __name__ == '__main__':
  Run('input/16.txt')