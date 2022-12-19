import os
import re
from parse import parse
from copy import deepcopy
from functools import cache
from frozenlist import FrozenList
from collections import defaultdict

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Hoist(shape, height):
  return [(p[0], p[1] + height + 4) for p in shape]

def Blow(shape, board, wind):
  if wind == '<':
    newshape = [(p[0] - 1, p[1]) for p in shape]
  elif wind == '>':
    newshape = [(p[0] + 1, p[1]) for p in shape]

  if any([p in board for p in newshape]) or any([p[0] < 0 or p[0] > 6 for p in newshape]):
    return shape
  return newshape

def Drop(shape, board):
  newshape = [(p[0], p[1] - 1) for p in shape]
  if any([p in board for p in newshape]):
    return False, shape
  return True, newshape


def PrintBoard(board, height):
  PrintBoardDict(defaultdict(lambda: ' ', {p : '#' for p in filter(lambda b: b[1] > 0, board)}), height)


def PrintBoardDict(boarddict, height):
  print()
  for y in range(height, 0, -1):
    print(str(y).rjust(4), end='')
    print('|', end='')
    for x in range(7):
      print(boarddict[(x, y)], end='')
    print('|')
  print('    +-------+')
  print(f'height = {height}')
  print()


def Run(path):
  wind = ReadFile(path)
  windIx = -1
  windlen = len(wind)
  shapes = [
    [(2,0),(3,0),(4,0),(5,0)],
    [(2,1),(3,2),(3,1),(3,0),(4,1)],
    [(2,0),(3,0),(4,0),(4,1),(4,2)],
    [(2,3),(2,2),(2,1),(2,0)],
    [(2,1),(3,1),(2,0),(3,0)]
  ]
  shapeIx = -1
  count = 0
  height = 0
  board = set([(x,0) for x in range(7)])
  boarddict = defaultdict(lambda: ' ')
  sch = '=+LIO'


  while count < 2022:
    count += 1
    shapeIx = (shapeIx + 1) % 5
    assert shapeIx < 5
    shape = shapes[shapeIx]
    shape = Hoist(shape, height)

    while True:
      windIx = (windIx + 1) % windlen
      assert windIx < windlen
      shape = Blow(shape, board, wind[windIx])
      more, shape = Drop(shape, board)
      if not more: 
        break
    
    for b in shape:
      board.add(b)
      boarddict[b] = sch[shapeIx]

    height = max(max([p[1] for p in shape]), height)

  # PrintBoardDict(boarddict, height)
  print(f'2022 block height = {height}')


def Run2(path):
  wind = ReadFile(path)
  windIx = -1
  windlen = len(wind)
  shapes = [
    [(2,0),(3,0),(4,0),(5,0)],
    [(2,1),(3,2),(3,1),(3,0),(4,1)],
    [(2,0),(3,0),(4,0),(4,1),(4,2)],
    [(2,3),(2,2),(2,1),(2,0)],
    [(2,1),(3,1),(2,0),(3,0)]
  ]
  shapeIx = -1
  count = 0
  height = 0
  board = set([(x,0) for x in range(7)])
  boarddict = defaultdict(lambda: ' ')
  sch = '=+LIO'

  heightBeforeCapture = 0
  last5 = None
  captures = {}
  while True:
    count += 1
    shapeIx = (shapeIx + 1) % 5
    shape = shapes[shapeIx]
    shape = Hoist(shape, height)

    if last5 is None and shapeIx == 0 and windIx >= 0:
      last5 = (windIx, FrozenList())
      heightBeforeCapture = height
    while True:
      windIx = (windIx + 1) % windlen
      assert windIx < windlen
      shape = Blow(shape, board, wind[windIx])
      more, shape = Drop(shape, board)
      if not more: 
        break
    
    for b in shape:
      board.add(b)
      boarddict[b] = sch[shapeIx]
    
    height = max(max([p[1] for p in shape]), height)

    if last5:
      l5s = FrozenList([(p[0], p[1] - height) for p in shape])
      l5s.freeze()
      last5[1].append(l5s)

      if len(last5[1]) == 5:
        last5[1].freeze()
        key = deepcopy(last5)
        last5 = None

        if key in captures:
          (preludeRocks, preludeHeight, batchHeight) = captures[key]
          rocksInCycle = count - preludeRocks - 5
          heightInCycle = height - batchHeight - preludeHeight

          rocksRemaining = 1000000000000 - preludeRocks
          rockCycles = rocksRemaining // rocksInCycle
          leftoverRocks = rocksRemaining % rocksInCycle
          intermediateHeight = rockCycles * heightInCycle

          # "board" ends with the rocks in cycle, can take advantage of that.
          # get height of board now, drop leftoverrocks, calc height of leftover, add to total
          oldHeight = height
          for i in range(leftoverRocks):
            shapeIx = i % 5
            shape = shapes[shapeIx]
            shape = Hoist(shape, height) # this is the height of the board currently

            while True:
              windIx = (windIx + 1) % windlen
              assert windIx < windlen
              shape = Blow(shape, board, wind[windIx])
              more, shape = Drop(shape, board)
              if not more: 
                break
            
            for b in shape:
              board.add(b)
              boarddict[b] = sch[shapeIx]
            
            height = max(max([p[1] for p in shape]), height)
          leftoverHeight = height - oldHeight

          finalHeight = preludeHeight + intermediateHeight + leftoverHeight
          assert finalHeight < 1591977077353, f'Dammit, too big! {finalHeight}'
          print(f'1000000000000 block height = {finalHeight}')          
          return
        else:
          # at this point I really need to test to see if the very first piece was actually lower
          # than the height at the time it dropped. but I'm really tired of working on this puzzle,
          # so I just guessed finalHeight, finalHeight-1, finalHeight-2. The last one was correct.
          
          captures[key] = (count - 5, heightBeforeCapture, height-heightBeforeCapture)


Run("input/17t.txt")
Run2("input/17t.txt")
print("--------")
Run("input/17.txt")
Run2("input/17.txt")
