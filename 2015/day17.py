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

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Run(path, amt):
  containers = [int(v) for v in ReadFile(path).splitlines()]
  total = 0
  for ix in range(1, len(containers) + 1):
    total += len(list(filter(lambda c: sum(c) == amt, combinations(containers, ix))))
  return total

def Run2(path, amt):
  containers = [int(v) for v in ReadFile(path).splitlines()]
  for ix in range(1, len(containers) + 1):
    rez = len(list(filter(lambda c: sum(c) == amt, combinations(containers, ix))))
    if rez > 0: return rez



if __name__ == '__main__':
  assert Run('input/17t.txt', 25) == 4, Run('input/17t.txt', 25)
  print(Run('input/17.txt', 150))
  assert Run2('input/17t.txt', 25) == 3, Run2('input/17t.txt', 25)
  print(Run2('input/17.txt', 150))  