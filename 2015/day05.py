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

def Check(l):
  vowels = 0
  double = False
  lastc = None
  for c in l:
    if c in 'aeiou': 
      vowels += 1
    if lastc:
      if c == lastc:
        double = True
      if f'{lastc}{c}' in ['ab', 'cd', 'pq', 'xy']:
        return False
    lastc = c
  return double and vowels >= 3

def Check2(l: str):
  hurdle = False
  for ix in range(2,len(l)):
    if l[ix] == l[ix - 2]:
      hurdle = True
      break
  if not hurdle: return False
  for ix in range(len(l) - 1):
    pair = l[ix:ix+2]
    if len(l.split(pair)) > 2:
      return True
  return False

def Run(path):
  count = 0
  for l in ReadFile(path).splitlines():
    if Check(l): count += 1
  print(count)

  count = 0
  for l in ReadFile(path).splitlines():
    if Check2(l): count += 1
  print(count)

if __name__ == '__main__':
  Run('input/05.txt')

