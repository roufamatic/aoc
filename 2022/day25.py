from __future__ import annotations
import os
import math
from typing import List,Dict
from parse import parse
from collections import deque
from copy import deepcopy
from functools import cache
import heapq

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output


def Run(path):
  lines=ReadFile(path).split('\n')
  sum = 0
  for line in lines:
    mysum = 0
    for v in line:
      mysum = 5 * mysum
      if v in '012':
        mysum += int(v)
      elif v == '-':
        mysum -= 1
      elif v == '=':
        mysum -= 2
    sum += mysum
  print(sum)

  
  # 12 == 22
  # 13 == 1==
  # 14 == 1=-
  # 15 == 1=0

  snafu = {'0':0,'1':1,'2':2,'-':-1,'=':-2}
  bsnafu = {0:'0',1:'1',2:'2',3:'=1', 4:'-1', 5:'01', 6:'11', 7:'21'} # reverse order for 3-7 !
  output = ['0']  
  work = sum
  place = -1
  while work > 0:
    place += 1
    d = work % 5
    if place < len(output):
      d = snafu[output.pop()] + d
    output.extend(bsnafu[d])
    work //= 5
  output.reverse()
  print(''.join(output))

if __name__ == '__main__':
  Run("input/25t.txt")
  print("--------")
  Run("input/25.txt")
