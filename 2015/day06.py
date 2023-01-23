import os
from parse import search
from copy import deepcopy
from collections import defaultdict

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def TurnOn(x1, y1, x2, y2):
  def o(x, y, last):
    if x in range(x1, x2+1) and y in range(y1, y2+1):
      return True
    else:
      return last
  return o

def TurnOff(x1, y1, x2, y2):
  def o(x, y, last):
    if x in range(x1, x2+1) and y in range(y1, y2+1):
      return False
    else:
      return last
  return o

def Toggle(x1, y1, x2, y2):
  def o(x, y, last):
    if x in range(x1, x2+1) and y in range(y1, y2+1):
      return not last
    else:
      return last
  return o

def TurnOn2(x1, y1, x2, y2):
  def o(x, y, last):
    if x in range(x1, x2+1) and y in range(y1, y2+1):
      return last + 1
    else:
      return last
  return o

def TurnOff2(x1, y1, x2, y2):
  def o(x, y, last):
    if x in range(x1, x2+1) and y in range(y1, y2+1):
      return max(last - 1, 0)
    else:
      return last
  return o

def Toggle2(x1, y1, x2, y2):
  def o(x, y, last):
    if x in range(x1, x2+1) and y in range(y1, y2+1):
      return last + 2
    else:
      return last
  return o

def Run(path):
  ops = [TurnOff(0, 999, 0, 999)]

  for line in ReadFile(path).splitlines():
    (x1,y1,x2,y2) = search('{:d},{:d} through {:d},{:d}', line)      
    if line.startswith("turn on"):
      ops.append(TurnOn(x1, y1, x2, y2))
    elif line.startswith("turn off"):
      ops.append(TurnOff(x1, y1, x2, y2))
    else:
      ops.append(Toggle(x1, y1, x2, y2))

  count = 0
  for x in range(1000):
    for y in range(1000):
      last = False
      for op in ops:
        last = op(x, y, last)
      if last: count+=1

  # 377366 too low
  print(count)

  ops = [TurnOff(0, 999, 0, 999)]

  for line in ReadFile(path).splitlines():
    (x1,y1,x2,y2) = search('{:d},{:d} through {:d},{:d}', line)      
    if line.startswith("turn on"):
      ops.append(TurnOn2(x1, y1, x2, y2))
    elif line.startswith("turn off"):
      ops.append(TurnOff2(x1, y1, x2, y2))
    else:
      ops.append(Toggle2(x1, y1, x2, y2))

  brightness = 0
  for x in range(1000):
    for y in range(1000):
      last = 0
      for op in ops:
        last = op(x, y, last)
      brightness += last

  print(brightness)


if __name__ == '__main__':
  Run('input/06.txt')

