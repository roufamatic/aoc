import os
from parse import parse
from copy import deepcopy
from collections import defaultdict
from frozendict import frozendict
from frozenlist import FrozenList
from functools import cache, reduce
import heapq
import math
import json
from itertools import permutations

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

#@cache
def MaximizeRecurse(ingredients: FrozenList, amountRemaining: int, current: FrozenList, calorize = False):
  if len(ingredients) == 1:
    ing = ingredients[0]
    cur = FrozenList(current)
    cur.append((ing[1] * amountRemaining, ing[2] * amountRemaining, ing[3] * amountRemaining, ing[4] * amountRemaining, ing[5] * amountRemaining))
    
    if calorize and sum([ingr[4] for ingr in cur]) != 500:
      return 0

    # sum it up and return.
    output = [0, 0, 0, 0]
    for ing in cur:
      for i in range(4):
        output[i] += ing[i]
    if any(filter(lambda z: z < 0, output)):
      return 0
    return max(0, reduce(lambda a,b:a*b, output, 1))
  else:
    fl = FrozenList(ingredients)
    ing = fl.pop()
    fl.freeze()
    best = 0
    for rm in range(1, amountRemaining - len(fl) + 1):
      cur = FrozenList(current)
      cur.append((ing[1] * rm, ing[2] * rm, ing[3] * rm, ing[4] * rm, ing[5] * rm))
      cur.freeze()
      best = max(best, MaximizeRecurse(fl, amountRemaining - rm, cur, calorize))
    return best

def Maximize(ingredients: FrozenList):
  fl2 = FrozenList()
  fl2.freeze()
  return [MaximizeRecurse(ingredients, 100, fl2), MaximizeRecurse(ingredients, 100, fl2, True)] 

def Run(path):
  ingredients = FrozenList()
  for l in ReadFile(path).splitlines():
    ingredients.append(tuple( parse('{}: capacity {:d}, durability {:d}, flavor {:d}, texture {:d}, calories {:d}', l)))
  ingredients.freeze()
  return Maximize(ingredients)


if __name__ == '__main__':
  t = Run('input/15t.txt')
  assert t[0] == 62842880 and t[1] == 57600000, t
  print(Run('input/15.txt'))
