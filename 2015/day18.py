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

def Neighbors(pt, maxx, maxy):
  o = set()
  (x,y) = pt
  for x1 in range(x-1,x+2):
    for y1 in range(y-1,y+2):
      if x1 < 0 or x1 > maxx or y1 < 0 or y1 > maxy or (x1,y1) == pt: continue
      o.add((x1,y1))
  return o

def Run(path, steps, stuck = False):
  lights = set()
  lines = ReadFile(path).splitlines()
  maxy = len(lines) - 1
  maxx = len(lines[0]) - 1
  for y, row in enumerate(lines):
    for x, c in enumerate(row):
      if c == '#':
        lights.add((x,y))
  if stuck:
    lights.add((0,0))
    lights.add((0,maxy))
    lights.add((maxx,0))
    lights.add((maxx,maxy))
  for _ in range(steps):
    l = set()
    for x in range(maxx+1):
      for y in range(maxy+1):
        neighbors = Neighbors((x,y), maxx, maxy)
        if (x,y) in lights:
          if len(neighbors & lights) in (2,3):
            l.add((x,y))
        else:
          if len(neighbors & lights) == 3:
            l.add((x,y))
    lights = l
    if stuck:
      lights.add((0,0))
      lights.add((0,maxy))
      lights.add((maxx,0))
      lights.add((maxx,maxy))
  return len(lights)          

if __name__ == '__main__':
  assert Run('input/18t.txt', 4) == 4, Run('input/18t.txt', 4)
  print(Run('input/18.txt', 100))
  assert Run('input/18t.txt', 5, True) == 17, Run('input/18t.txt', 5, True)
  print(Run('input/18.txt', 100, True))  