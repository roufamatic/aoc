from __future__ import annotations
import os
from typing import List,Dict
from parse import parse
from collections import deque
from frozenlist import FrozenList

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Run(path, mult=1, mixes = 1):
  orig = FrozenList()
  d = deque()
  zero = ()
  for ix,l in enumerate(ReadFile(path).splitlines()):
    v = int(l) * mult
    orig.append(v)
    d.append((ix, v))
    if v == 0:
      zero = (ix, v)
  orig.freeze() # immutable so I can't muck it up!
  assert zero in d

  #print(d)
  for _ in range(mixes):
    for ix, v in enumerate(orig):
      if v == 0: continue
      # place v at index 0.
      d.rotate(-d.index((ix, v)))
      # remove v from the deque.
      d.popleft()
      # rotate the deque so the correct position is before index 0.
      d.rotate(-v)
      # place v at index 0.
      d.appendleft((ix, v))
    assert zero in d
  
  d.rotate(-d.index(zero))
  result = 0
  for _ in range(3):
    d.rotate(-1000)
    print(d[0])
    result += d[0][1]

  print(f'result = {result}')

if __name__ == '__main__':
  Run("input/20t.txt")
  print("--------")
  Run("input/20.txt")
  print("--------")
  print("--------")
  Run("input/20t.txt", 811589153, 10)
  print("--------")
  Run("input/20.txt", 811589153, 10)
