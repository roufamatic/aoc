import os
from parse import search
from copy import deepcopy
from collections import defaultdict
from frozendict import frozendict
from frozenlist import FrozenList
from functools import cache
import heapq
import math
import json

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Summify(x):
  total = 0
  if type(x) == dict:
    if 'red' not in x.values():
      for v in x.values():
        if type(v) == int:
          total += v
        elif type(v) in (dict, list):
          total += Summify(v)
  elif type(x) == list:
    for v in x:
      if type(v) in (dict, list):
        total += Summify(v)
      elif type(v) == int:
        total += v
  return total


def Run(path):
  s = ReadFile(path)
  total = 0
  working = ''
  for c in s:
    if c in '-0123456789':
      working += c
    elif working != '':
      total += int(working)
      working = ''
  print(total)

  j = json.loads(s)
  print(Summify(j))



if __name__ == '__main__':
  Run('input/12.txt')