import os
from parse import search
from copy import deepcopy
from collections import defaultdict
from frozendict import frozendict
from frozenlist import FrozenList
from functools import cache
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


def Score(perm, peeps):
  total = 0
  for ix in range(len(perm)):
    fwd = (ix + 1) % len(perm)
    bck = (ix - 1) % len(perm)
    total += peeps[perm[ix]][perm[fwd]] + peeps[perm[ix]][perm[bck]]
  return total

def Run(path, addme = False):
  peeps = defaultdict(lambda: {})
  for line in ReadFile(path).splitlines():
    bits = line.split(' ')
    p1 = bits[0]
    p2 = bits[-1][:-1]
    amt = int(next(filter(lambda v: v[0] in '0123456789', bits)))
    if 'lose' in bits:
      amt = -amt
    peeps[p1][p2] = amt
  if addme:
    for p in list(peeps.keys()):
      peeps['me'][p] = 0
      peeps[p]['me'] = 0

  best = max([Score(p, peeps) for p in permutations(peeps.keys())])
  return best



if __name__ == '__main__':
  assert Run('input/13t.txt') == 330, Run('input/13t.txt')
  print(Run('input/13.txt'))
  print(Run('input/13.txt', True))
