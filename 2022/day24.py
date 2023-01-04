from __future__ import annotations
import os
import math
from typing import List,Dict
from parse import parse
from collections import deque
from copy import deepcopy
from functools import cache
import heapq

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output


def Run(path):
  allblizzards = []
  walls = set()
  lines=ReadFile(path).split('\n')
  start = None
  end = None
  for y, l in enumerate(lines):
    for x, c in enumerate(l):
      if c == '.' and y == 0:
        start = (x,y)
      elif c == '.' and y == len(lines) - 1:
        end = (x,y)
      elif c == '#':
        walls.add((x,y))
      elif c in '<^v>':
        assert (x,y,c) not in allblizzards
        allblizzards.append((x,y,c))
  walls.add((start[0], -1))
  walls.add((end[0], end[1] + 1))
  
  blizmoves = {'^': (0,-1), 'v':(0,1), '<':(-1,0), '>':(1,0)}
  moves = [(0,-1),(0,1),(-1,0),(1,0),(0,0)]
  
  @cache
  def MoveBlizzards(steps):
    maxx = len(lines[0]) - 2
    maxy = len(lines) - 2

    wsteps = steps % maxx
    hsteps = steps % maxy

    output = set()
    for b in allblizzards:
      x = b[0]
      y = b[1]
      bm = blizmoves[b[2]]
      if b[2] in '<>':
        for _ in range(wsteps):
          x += bm[0]
          if x == 0: x = maxx
          elif x > maxx: x = 1
      else:
        for _ in range(hsteps):
          y += bm[1]
          if y == 0: y = maxy
          elif y > maxy: y = 1
      output.add((x,y))
    return output

  def Manhattan(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

  def Go(initialSteps, s, e):
    # (score, (x, y), moves)
    q = [(math.inf, s, initialSteps)]
    seen = set(q)
    while True:
      lastmove = heapq.heappop(q)
      pos = lastmove[1]
      steps = lastmove[2] + 1
      # Move the blizzards first
      blizzards = MoveBlizzards(steps)
      # Then explore all the safe places to move to.
      for m in moves:
        newp = (pos[0] + m[0], pos[1] + m[1])
        if newp == e:
          print(f'Reached goal in {steps} steps')
          return steps
        if newp in walls:
          continue
        if newp in blizzards:
          continue
        score = steps + Manhattan(newp, end)
        item = (score, newp, steps)
        if item not in seen:
          heapq.heappush(q, item)
          seen.add(item)

  best = Go(0, start, end)
  best = Go(best, end, start)
  best = Go(best, start, end)
  print(f'total steps = {best}')

if __name__ == '__main__':
  Run("input/24t.txt")
  print("--------")
  Run("input/24.txt")
