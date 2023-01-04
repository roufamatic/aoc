from __future__ import annotations
import os
from typing import List,Dict
from parse import parse
from collections import deque
from copy import deepcopy
from functools import cache

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Neighbors(pos, d = None):
  if d and d[0] != 0:
    xr = [d[0]]
  else:
    xr = range(-1, 2)
  if d and d[1] != 0:
    yr = [d[1]]
  else:
    yr = range(-1, 2)  
  
  for y in yr:
    for x in xr:
      if y == 0 and x == 0: 
        continue
      yield (pos[0] + x, pos[1] + y)

def Run(path):
  N = (0,-1)
  S = (0, 1)
  W = (-1,0)
  E = (1, 0)
  directions = deque([N,S,W,E])
  elves = set()
  lines=ReadFile(path).split('\n')
  for y, line in enumerate(lines):
    for x, val in enumerate(line):
      if val == '#':
        elves.add((x,y))
  
  i = 0
  while True:
    i += 1
    consider = list(filter(lambda p: any(n in elves for n in Neighbors(p)), elves))
    if len(consider) == 0:
      print(f'part 2: round {i}')
      break
    proposals = {}
    for d in directions:
      leftovers = []
      for p in consider:
        if not any(n in elves for n in Neighbors(p, d)):
          prop = (p[0] + d[0], p[1] + d[1])
          if prop not in proposals:
            proposals[prop] = p
          else:
            proposals.pop(prop)
        else:
          leftovers.append(p)
      consider = leftovers
    for k,v in proposals.items():
      elves.remove(v)
      elves.add(k)
    directions.rotate(-1)
  
    if i == 10:
      minx = min([e[0] for e in elves])
      miny = min([e[1] for e in elves])
      maxx = max([e[0] for e in elves]) + 1
      maxy = max([e[1] for e in elves]) + 1
      total = (maxx-minx) * (maxy-miny) - len(elves) 
      print(f'part 1: total = {total}')



if __name__ == '__main__':
  Run("input/23t.txt")
  print("--------")
  Run("input/23.txt")
