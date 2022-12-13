import os
from parse import parse
from copy import deepcopy
import ast
from functools import cmp_to_key

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def EvalRecurse(left, right):
  for i in range(max(len(left), len(right))):
    if i in range(len(left)):
      lval = left[i]
    else:
      return True
    rval = None
    if i in range(len(right)):
      rval = right[i]
    else:
      return False

    if type(lval) == int and type(rval) == int:
      if lval < rval:
        return True
      if lval > rval:
        return False
      else:
        continue
    elif type(lval) == int and type(rval) == list:
      lval = [lval]
    elif type(rval) == int and type(lval) == list:
      rval = [rval]
    
    inner = EvalRecurse(lval, rval)
    if inner == None:
      continue
    return inner
    
  return None
      

def Eval(pair):
  (l, r) = pair
  
  left = ast.literal_eval(l)
  right = ast.literal_eval(r)

  return EvalRecurse(left, right)

def Run(path):
  input = ReadFile(path)
  pairs = [tuple(i.split('\n')) for i in input.split('\n\n')]
  
  total = 0
  for ix in range(1, len(pairs) + 1):
    if Eval(pairs[ix - 1]):
      # print(f'pair {ix} works!')
      total += ix
  print(total)

  dividers = ['[[2]]', '[[6]]']
  lines = list(filter(lambda i: i != '', input.split('\n')))
  lines.extend(dividers)
  
  compare = lambda str1, str2: -1 if Eval((str1, str2)) else 1
  lines.sort(key=cmp_to_key(compare))

  total = 1
  for ix, line in enumerate(lines):
    if line in dividers:
      total *= (ix + 1)
  print(total)

Run("input/13t.txt")
print("--------")
Run("input/13.txt")

