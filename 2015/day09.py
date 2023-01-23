import os
from parse import search
from copy import deepcopy
from collections import defaultdict
from frozendict import frozendict
from frozenlist import FrozenList
from functools import cache
import heapq
import math

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def BestFrom(m:frozendict, a:str, visited: frozenset, path: list):
  score = math.inf
  myvisited = set(visited)
  myvisited.add(a)
  path.append(a)
  outputpath = path.copy()
  for d in m[a]:
    if d[1] in visited: continue
    rez = BestFrom(m, d[1], frozenset(myvisited), path.copy())
    myscore = d[0] + rez[0]
    if myscore < score:
      score = myscore
      outputpath = rez[1]
  return (0, outputpath) if score == math.inf else (score, outputpath)

def WorstFrom(m:frozendict, a:str, visited: frozenset, path: list):
  score = 0
  myvisited = set(visited)
  myvisited.add(a)
  path.append(a)
  outputpath = path.copy()
  for d in m[a]:
    if d[1] in visited: continue
    rez = WorstFrom(m, d[1], frozenset(myvisited), path.copy())
    myscore = d[0] + rez[0]
    if myscore > score:
      score = myscore
      outputpath = rez[1]
  return (score, outputpath)

def Run(path):
  m = defaultdict(lambda: FrozenList())
  
  for l in ReadFile(path).splitlines():
    s1 = l.split(' = ')
    a,b = s1[0].split(' to ')
    val = int(s1[1])
    m[a].append((val, b))
    m[b].append((val, a))

  for v in m.values():
    v.freeze()
  
  fz = frozendict(m)
  
  best = math.inf
  worst = 0
  bestpath = None
  worstpath = None

  for s in m.keys():
    mybest, path = BestFrom(fz, s, frozenset(), [])
    if mybest < best:
      best = mybest
      bestpath = path.copy()
    myworst, path = WorstFrom(fz, s, frozenset(), [])
    if myworst > worst:
      worst = myworst
      worstpath = path.copy()
  assert(len(bestpath) == len(m))
  print(f'BEST: steps:{best}, path:{bestpath}')
  print(f'WORST: steps:{worst}, path:{worstpath}')

if __name__ == '__main__':
  Run('input/09t.txt')
  print('----')
  Run('input/09.txt')
