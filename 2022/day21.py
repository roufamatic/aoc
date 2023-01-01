from __future__ import annotations
import math
import os
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

def Eval(monkey, mkys):
  m = mkys[monkey]
  if type(m) == int:
    return m
  fn = m[0]
  args = tuple(m[1])
  return fn(*args,mkys)

def Run(path):
  monkeys = {}
  ops = {
    '+':lambda x,y,mkys: Eval(x,mkys)+Eval(y,mkys),
    '-':lambda x,y,mkys: Eval(x,mkys)-Eval(y,mkys),
    '*':lambda x,y,mkys: Eval(x,mkys)*Eval(y,mkys),
    '/':lambda x,y,mkys: Eval(x,mkys)/Eval(y,mkys),
  }
  for line in ReadFile(path).splitlines():
    info:List[str] = line.split(': ')
    # print(info)
    monkey:str = info[0]
    job:str = info[1]
    foundOp = False
    for o in '+-*/':
      if o in job:
        foundOp = True
        operands:tuple[str] = (p.strip() for p in job.split(o))
        monkeys[monkey] = (ops[o], operands)
        break
    if not foundOp:
      monkeys[monkey] = int(job)

  print(Eval('root', frozendict(monkeys)))


def Run2(path):
  monkeys = {}
  ops = {
    '+':lambda x,y,mkys: Eval(x,mkys)+Eval(y,mkys),
    '-':lambda x,y,mkys: Eval(x,mkys)-Eval(y,mkys),
    '*':lambda x,y,mkys: Eval(x,mkys)*Eval(y,mkys),
    '/':lambda x,y,mkys: Eval(x,mkys)/Eval(y,mkys),
    '=':lambda x,_: x
  }
  for line in ReadFile(path).splitlines():
    info:List[str] = line.split(': ')
    # print(info)
    monkey:str = info[0]
    job:str = info[1]
    foundOp = False
    if monkey == 'humn':
      # no entry for humans
      continue
    if monkey == 'root':
      monkeys[monkey] = tuple(job.split(' + '))
      continue
    for o in '+-*/':
      if o in job:
        foundOp = True
        operands:tuple[str] = tuple(p.strip() for p in job.split(o))
        monkeys[monkey] = (ops[o], operands, o)
        break
    if not foundOp:
      monkeys[monkey] = (ops['='], (int(job),), o)
  

  left,right = monkeys['root']
  lval = None
  rval = None
  try:
    goal = Eval(left, monkeys)
  except:
    pass

  try:
    rval = Eval(right, monkeys)
  except:
    pass

  assert lval is not None or rval is not None
  if lval is None:
    goal = rval
    start = left
  else:
    goal = lval
    start = right

  assert type(goal) in (float,int), f'type == {type(lval)}'
  
  H = 'humn'

  def Qval(v):
    monkeys[H] = v
    return Eval(start, monkeys)


  if Qval(0) > Qval(1):
    cmp = lambda a,b: a > b
  else:
    cmp = lambda a,b: b > a
  def findHumn():
    if (Qval(0) == goal):
      return 0
    # hoping this increases monotonically... no guarantee though!
    i = 1
    while cmp(Qval(i), goal):
      i *= 2
    return binarySearch(min(i // 2, i), max(i // 2, i))

  def binarySearch(low, high):
    if (high >= low):
      mid = (low + high)//2
      if Qval(mid) == goal:
        return mid
      if cmp(Qval(mid), goal):
        return binarySearch(mid, high)
      else:
        return binarySearch(low, mid)
    return -1
  print(findHumn())

if __name__ == '__main__':
  Run("input/21t.txt")
  print("--------")
  Run("input/21.txt")
  print("--------")
  print("--------")
  Run2("input/21t.txt")
  print("--------")
  Run2("input/21.txt")
