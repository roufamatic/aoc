from __future__ import annotations
import math
import os
from copy import deepcopy
from typing import List,Dict
from parse import parse
from collections import deque
from frozendict import frozendict
from functools import cache

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Run(path):
  griddle, instrux = ReadFile(path).split('\n\n')
  grid = [list(v) for v in griddle.splitlines()]
  pos = (grid[0].index('.'), 0)
  R = (1, 0)
  D = (0, 1)
  L = (-1, 0)
  U = (0, -1)

  dirs = [R, D, L, U]
  
  def Walk(start, dist, d):
    output = start
    probe = start
    moves = 0
    while moves < dist:
      x, y = (probe[0] + d[0], probe[1] + d[1])
      if y < 0 and d == U:
        y = len(grid) - 1
      elif y > len(grid) - 1 and d == D:
        y = 0
      if x < 0 and d == L:
        x = len(grid[y]) - 1
      elif x > len(grid[y]) - 1 and d == R:
        x = 0

      if x >= len(grid[y]):
        probe = (x,y)
      elif grid[y][x] == '#':
        return output
      elif grid[y][x] == '.':
        output = (x,y)
        probe = output
        moves += 1
      else:
        probe = (x,y)
    return output

  dist = 0
  dirIx = 0
  for ch in instrux:
    if ch in 'LR':
      pos = Walk(pos, dist, dirs[dirIx])
      dist = 0
      if ch == 'L':
        dirIx = (dirIx - 1) % 4
      else:
        dirIx = (dirIx + 1) % 4
    else:
      dist = dist * 10 + int(ch)
  if dist:
    pos = Walk(pos, dist, dirs[dirIx])
  print((pos[1]+1)*1000 + (pos[0]+1)*4 + dirIx)  


def Run2(path):
  griddle, instrux = ReadFile(path).split('\n\n')
  gridarr = [list(v) for v in griddle.splitlines()]
  pos = (gridarr[0].index('.'), 0)
  R = (1, 0)
  D = (0, 1)
  L = (-1, 0)
  U = (0, -1)

  def PrintGrid(pos, d):
    for y in range(len(gridarr)):
      for x, v in enumerate(gridarr[y]):
        if (x,y) == pos:
          if d == U: print('^',end='')
          elif d == D: print('v', end='')
          elif d == L: print('<', end='')
          else: print('>', end='')
        else:
          print(v, end='')
      print()

  # convert grid to dict (easier to work with, hopefully)
  grid = {}
  for y in range(len(gridarr)):
    for x, v in enumerate(gridarr[y]):
      if v not in '.#': continue
      grid[(x, y)] = v

  dirs = [R, D, L, U]

  # hardcoded to the real data :-(  
  def Warp(x, y, d):
    if d == U:
      if x in range(0, 50) and y == 99: # left -> front
        return 50, x + 50, R
      if x in range(50,100) and y == -1: # top -> back
        return 0, x + 100, R
      if x in range(100,150) and y == -1: # right -> back
        return x - 100, 199, U
      assert False
    if d == D:
      if x in range(0, 50) and y == 200: # back -> right
        return x + 100, 0, D
      if x in range(50, 100) and y == 150: # bottom -> back
        return 49, x + 100, L
      if x in range(100,150) and y == 50: # right -> front
        return 99, x - 50, L
      assert False
    if d == L:
      if y in range(0, 50) and x == 49: # top -> left
        return 0, 149 - y, R
      if y in range(50, 100) and x == 49: # front -> left
        return y - 50, 100, D
      if y in range(100, 150) and x == -1: # left -> top
        return 50, 149 - y, R
      if y in range(150, 200) and x == -1: # back -> top
        return y - 100, 0, D
      assert False
    if d == R:
      if y in range(0, 50) and x == 150: # right -> bottom 
        return 99, 149 - y, L
      if y in range(50, 100) and x == 100: # front -> right
        return y + 50, 49, U
      if y in range(100, 150) and x == 100: # bottom -> right
        return 149, 149 - y, L
      if y in range(150, 200) and x == 50: # back -> bottom
        return y - 100, 149, U
      assert False
    assert False, f'direction = {d} ?'



  def Walk(start, dist, d):
    output = start
    probe = start
    moves = 0
    while moves < dist:
      x, y = (probe[0] + d[0], probe[1] + d[1])
      d2 = d
      if (x,y) not in grid:
        x, y, d2 = Warp(x, y, d)
      if grid[(x,y)] == '#':
        return (output, d)
      elif grid[(x,y)] == '.':
        output = (x,y)
        probe = output
        moves += 1
        d = d2
      else:
        probe = (x,y)
    return (output, d)

  dist = 0
  dirIx = 0
  for ch in instrux:
    if ch in 'LR':
      (pos, d) = Walk(pos, dist, dirs[dirIx])
      dirIx = dirs.index(d)
      dist = 0
      if ch == 'L':
        dirIx = (dirIx - 1) % 4
      else:
        dirIx = (dirIx + 1) % 4
      #PrintGrid(pos, d)
    else:
      dist = dist * 10 + int(ch)
  if dist:
    (pos, d) = Walk(pos, dist, dirs[dirIx])
    dirIx = dirs.index(d)
  print((pos[1]+1)*1000 + (pos[0]+1)*4 + dirIx)  
  


if __name__ == '__main__':
  Run("input/22t.txt")
  print("--------")
  Run("input/22.txt")
  print("--------")
  print("--------")
  # Run2("input/22t.txt")
  # print("--------")
  Run2("input/22.txt")
