import os
from parse import parse
from copy import deepcopy


def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def nextpos(grainpos, rocks, bottom = -1):
  y = grainpos[1] + 1
  if y == bottom:
    return None
  desired = (grainpos[0], y)
  if desired[1] == bottom:
    return None
  if desired not in rocks:
    return desired
  desired = (grainpos[0] - 1, y)
  if desired not in rocks:
    return desired
  desired = (grainpos[0] + 1, y)
  if desired not in rocks:
    return desired
  return None


def Run(path):
  input = ReadFile(path)
  
  rocks = set()
  for line in input.split('\n'):
    bits = line.split(' -> ')
    lastpair = None
    for bit in bits:
      pair = tuple([int(b) for b in bit.split(',')])
      if lastpair is None:
        rocks.add(pair)
      else:
        if lastpair[0] <= pair[0]:
          for x in range(lastpair[0], pair[0] + 1):
            rocks.add((x, lastpair[1]))
        else:
          for x in range(pair[0], lastpair[0] + 1):
            rocks.add((x, lastpair[1]))

        if lastpair[1] <= pair[1]:
          for y in range(lastpair[1], pair[1] + 1):
            rocks.add((lastpair[0], y))
        else:
          for y in range(pair[1], lastpair[1] + 1):
            rocks.add((lastpair[0], y))
      lastpair = pair

  p1rocks = deepcopy(rocks)
  # start simulating!
  bottom = max([pair[1] for pair in p1rocks])
  
  units = 0
  done = False
  while not done:
    s = (500, 0)
    while (g := nextpos(s, p1rocks)):
      if g[1] > bottom:
        print(units)
        done = True
        break
      s = g
    units += 1
    p1rocks.add(s)

  units = 0
  # part 2
  p2rocks = deepcopy(rocks)
  done = False
  while not done:
    s = (500, 0)
    while (g := nextpos(s, p2rocks, bottom + 2)):
      s = g
    if s == (500, 0):
      print(units + 1)
      done = True
      break
    units += 1
    p2rocks.add(s)

Run("input/14t.txt")
print("--------")
Run("input/14.txt")
