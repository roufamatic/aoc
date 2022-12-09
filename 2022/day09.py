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

def MoveHead(dir, curpos):
  if dir == 'R':
    return (curpos[0] + 1, curpos[1])
  elif dir == 'L':
    return (curpos[0] - 1, curpos[1])
  elif dir == 'U':
    return (curpos[0], curpos[1] + 1)
  else:
    return (curpos[0], curpos[1] - 1)

def MoveTail(headpos, tailpos):
  (hx, hy) = headpos
  (tx, ty) = tailpos
  
  # diagonal!
  if hx != tx and hy != ty:
    if abs(hx - tx) == 2 and abs(hy - ty) == 2:
      if tx < hx:
        newtx = tx + 1
      else:
        newtx = tx - 1
      if ty < hy:
        newty = ty + 1
      else:
        newty = ty - 1
    else:
      if hx - tx == 2:
        newtx = tx + 1
        newty = hy
      elif hx - tx == -2:
        newtx = tx - 1
        newty = hy
      elif hy - ty == 2:
        newty = ty + 1
        newtx = hx
      elif hy - ty == -2:
        newty = ty - 1
        newtx = hx
      # otherwise do nothing.
      else:
        newtx = tx
        newty = ty
  else:
    if hx - tx == 2:
      newtx = tx + 1
    elif hx - tx == -2:
      newtx = tx - 1
    else:
      newtx = tx
    
    if hy - ty == 2:
      newty = ty + 1
    elif hy - ty == -2:
      newty = ty - 1
    else:
      newty = ty
  
  return (newtx, newty)


def Run(path):
  input = ReadFile(path)
  lines = [v.strip() for v in input.split('\n')]

  hpos = (0,0)
  tpos = (0,0)
  visited = set([hpos])
  
  for line in lines:
    (dir, dist) = parse('{} {:d}', line)
    for _ in range(1, dist + 1):
      hpos = MoveHead(dir, hpos)
      tpos = MoveTail(hpos, tpos)
      visited.add(tpos)
  
  print(len(visited))

  poslist = [(0,0)] * 10
  visited = set([(0,0)])
  for line in lines:
    (dir, dist) = parse('{} {:d}', line)
    for _ in range(1, dist + 1):
      poslist[0] = MoveHead(dir, poslist[0])
      for i in range(1, len(poslist)):
        poslist[i] = MoveTail(poslist[i-1], poslist[i])
      visited.add(poslist[9])

  print(len(visited))

Run("input/09t.txt")
print("--------")
Run("input/09.txt")

