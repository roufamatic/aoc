import os
from parse import search
from copy import deepcopy
from collections import defaultdict
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
  repsize = 0
  realsize = 0
  escsize = 0
  for line in ReadFile(path).splitlines():
    repsize += len(line)
    realsize += len(eval(line))
    escsize += 2 + len(line) + max(0,line.count('"')) + max(0, line.count('\\'))
  print(repsize - realsize)
  print(escsize - repsize)

if __name__ == "__main__":
  Run('input/08.txt')