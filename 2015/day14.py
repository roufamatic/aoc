import os
from parse import parse
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

def Run(path, racetime):
  best = 0
  for l in ReadFile(path).splitlines():
    reindeer, speed, time, resttime = parse('{} can fly {:d} km/s for {:d} seconds, but then must rest for {:d} seconds.', l)
    t = 0
    distance = 0
    while t < racetime:
      if t % (time + resttime) < time:
        distance += speed
      t += 1
    print(f'{reindeer}: {distance}')
    if distance > best:
      best = distance
  return best

def Run2(path, racetime):
  best = 0
  rd = {}
  for l in ReadFile(path).splitlines():
    reindeer, speed, time, resttime = parse('{} can fly {:d} km/s for {:d} seconds, but then must rest for {:d} seconds.', l)
    rd[(reindeer, speed, time, resttime)] = [0, 0]
  t = 0
  while t < racetime:
    for r, v in rd.items():
      (reindeer, speed, time, resttime) = r
      if t % (time + resttime) < time:
        v[1] += speed
    
    top = max(v[1] for v in rd.values())
    for v in rd.values():
      if v[1] == top:
        v[0] += 1
    t += 1
    
  top = max(v[0] for v in rd.values())
  for v in rd.values():
    if v[0] == top:
      return v[0]

if __name__ == '__main__':
  assert Run('input/14t.txt', 1000) == 1120, Run('input/14t.txt', 1000)
  print(Run('input/14.txt', 2503))
  print('---')
  assert Run2('input/14t.txt', 1000) == 689, Run2('input/14t.txt', 1000)
  print(Run2('input/14.txt', 2503))
