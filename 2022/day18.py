import os
import re
from parse import parse
from copy import deepcopy
from functools import cache
from frozenlist import FrozenList
from collections import defaultdict
from collections import deque

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Run(path):
  cubes = [(p[0],p[1],p[2]) for p in [parse('{:d},{:d},{:d}', l) for l in ReadFile(path).splitlines()]]

  # a cube has 6 faces.
  # a face is exposed if there is not another cube adjacent to the face.
  # if 2 numbers are the same and one is +- 1, then those are adjacent.
  # e.g. 0,0,0 and 1,0,0 : 10 sides are exposed.
  # factorial is NOT gonna fly.
  
  # place all cubes in a 3x3x3 grid.
  # look at each pair (x,y), (x,z), (y,z)
  # find all the faces with the lowest (unused dimension) and the highest (unused dimension)
  # add to total.

  minx = min([c[0] for c in cubes])
  maxx = max([c[0] for c in cubes])
  miny = min([c[1] for c in cubes])
  maxy = max([c[1] for c in cubes])
  minz = min([c[2] for c in cubes])
  maxz = max([c[2] for c in cubes])

  exposed = 0
  # x,y
  for x in range(minx, maxx + 1):
    for y in range(miny, maxy + 1):
      l = ['0'] * (maxz + 1)
      possible = [p[2] for p in filter(lambda p: p[0] == x and p[1] == y, cubes)]
      for z in possible:
        l[z] = '1'
      lstr = ''.join(l)
      if lstr[0] == '1':
        exposed += 1
      if lstr[len(lstr) - 1] == '1':
        exposed += 1
      exposed += lstr.count('10')
      exposed += lstr.count('01')
      
  # x,z
  for x in range(minx, maxx + 1):
    for z in range(minz, maxz + 1):
      l = ['0'] * (maxy + 1)
      possible = [p[1] for p in filter(lambda p: p[0] == x and p[2] == z, cubes)]
      for y in possible:
        l[y] = '1'
      lstr = ''.join(l)
      if lstr[0] == '1':
        exposed += 1
      if lstr[len(lstr) - 1] == '1':
        exposed += 1
      exposed += lstr.count('10')
      exposed += lstr.count('01')

  # y,z
  for y in range(miny, maxy + 1):
    for z in range(minz, maxz + 1):
      l = ['0'] * (maxx + 1)
      possible = [p[0] for p in filter(lambda p: p[1] == y and p[2] == z, cubes)]
      for x in possible:
        l[x] = '1'
      lstr = ''.join(l)
      if lstr[0] == '1':
        exposed += 1
      if lstr[len(lstr) - 1] == '1':
        exposed += 1
      exposed += lstr.count('10')
      exposed += lstr.count('01')

  print(exposed)
  ##### part 2
  exposed = 0
  cset = set(cubes)
  dd = defaultdict(lambda: -1)

  for x in range(minx-1, maxx+2):
    for y in range(miny-1, maxy+2):
      for z in range(minz-1, maxz+2):
        if (x,y,z) in cset:
          dd[(x,y,z)] = 1
        else:
          dd[(x,y,z)] = 0

  # BFS
  q = deque()
  start = list(filter(lambda k: dd[k]==0, dd.keys()))[0]
  q.append(start)
  print(start)
  contiguous_empties = set()
  while q:
    c = q.popleft()
    if c in contiguous_empties:
      continue
    if dd[c] == 0:
      contiguous_empties.add(c)
      q.append((c[0]-1, c[1], c[2]))
      q.append((c[0]+1, c[1], c[2]))
      q.append((c[0], c[1]-1, c[2]))
      q.append((c[0], c[1]+1, c[2]))
      q.append((c[0], c[1], c[2]-1))
      q.append((c[0], c[1], c[2]+1))
    elif dd[c] == 1:
      exposed += 1

  print(exposed)


Run("input/18t.txt")
print("--------")
Run("input/18.txt")
