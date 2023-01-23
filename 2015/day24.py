import math
import os
from itertools import combinations
from functools import reduce

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Run(path):
  packages = [int(i) for i in ReadFile(path).splitlines()]
  maxsum = sum(packages) // 3

  def prod(l):
    return reduce(lambda x,y: x*y, l, 1)

  # Goal is to sort things in such a way that we can exit the moment we find a candidate.  
  for i in range(1, len(packages) + 1):
    combos = list(filter(lambda p: sum(p) == maxsum, combinations(packages, i)))
    combos.sort(key=lambda c: (len(c),prod(c)))
    for c in combos:
      pkgs2 = set.difference(set(packages), set(c))
      for j in range(1, len(pkgs2) + 1):
        pkgs2combos = filter(lambda p: sum(p) == maxsum, combinations(pkgs2, j))
        for c2 in pkgs2combos:
          pkgs3 = set.difference(pkgs2, set(c2))
          if sum(pkgs3) == maxsum:
            return prod(c)

def Run2(path):
  packages = [int(i) for i in ReadFile(path).splitlines()]
  maxsum = sum(packages) // 4

  def prod(l):
    return reduce(lambda x,y: x*y, l, 1)

  # Goal is to sort things in such a way that we can exit the moment we find a candidate.  
  for i in range(1, len(packages) + 1):
    combos = list(filter(lambda p: sum(p) == maxsum, combinations(packages, i)))
    combos.sort(key=lambda c: (len(c),prod(c)))
    for c in combos:
      pkgs2 = set.difference(set(packages), set(c))
      for j in range(1, len(pkgs2) + 1):
        pkgs2combos = filter(lambda p: sum(p) == maxsum, combinations(pkgs2, j))
        for c2 in pkgs2combos:
          pkgs3 = set.difference(pkgs2, set(c2))
          for k in range(1, len(pkgs3) + 1):
            pkgs3combos = filter(lambda p: sum(p) == maxsum, combinations(pkgs3, k))
            for c3 in pkgs3combos:
              pkgs4 = set.difference(pkgs3, set(c3))
              if sum(pkgs4) == maxsum:
                return prod(c)


if __name__ == '__main__':
  x=Run('input/24t.txt')
  assert x == 99, x
  print(f'part 1: {Run("input/24.txt")}')
  print("----")
  x=Run2('input/24t.txt')
  assert x == 44, x
  print(f'part 2: {Run2("input/24.txt")}')
