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
  print(f'maxsum: {maxsum}')
  lowest_qe = math.inf
  for front_count in range(1, len(packages) - 1):
    if lowest_qe < math.inf:
      return lowest_qe
    front_combos = filter(lambda f: sum(f) == maxsum, combinations(packages, front_count))
    for f in front_combos:
      lpackages = sorted(list(set(packages).difference(set(f))))
      for left_count in range(1, len(lpackages)):
        print(f'{front_count}, {left_count}')
        left_combos = filter(lambda c: sum(c) == maxsum, combinations(packages, left_count))
        if not any(left_combos):
          continue
        lowest_qe = min(lowest_qe, reduce(lambda x, y: x*y, f, 1))

def Run2(path):
  packages = [int(i) for i in ReadFile(path).splitlines()]
  maxsum = sum(packages) // 4
  print(f'maxsum: {maxsum}')
  allcombos = []
  for i in range(1, len(packages) + 1):
    allcombos.extend(filter(lambda p: sum(p) == maxsum, combinations(packages, i)))
    print(f'total size = {len(allcombos)} after combos of size {i} were added.')
  print(f'found {len(allcombos)} combinations')
  def prod(l):
    return reduce(lambda x,y: x*y, l, 1)
  allcombos.sort(key=lambda c: (len(c),prod(c)))
  print(f'sorted')
  for c in allcombos:
    pkgs2 = set.difference(set(packages), set(c))
    pkgs2combos = []
    for i in range(1, len(pkgs2) + 1):
      pkgs2combos.extend(filter(lambda p: sum(p) == maxsum, combinations(pkgs2, i)))
    for c2 in pkgs2combos:
      pkgs3 = set.difference(pkgs2, set(c2))
      pkgs3combos = []
      for i in range(1, len(pkgs3) + 1):
        pkgs3combos.extend(filter(lambda p: sum(p) == maxsum, combinations(pkgs3, i)))
      for c3 in pkgs3combos:
        pkgs4 = set.difference(pkgs3, set(c3))
        if sum(pkgs4) == maxsum:
          return prod(c)


  # lowest_qe = math.inf
  # for front_count in range(1, len(packages) - 2):
  #   if lowest_qe < math.inf:
  #     return lowest_qe
  #   front_combos = filter(lambda f: sum(f) == maxsum, combinations(packages, front_count))
  #   for f in front_combos:
  #     lpackages = sorted(list(set(packages).difference(set(f))))
  #     for left_count in range(1, len(lpackages)-1):
  #       left_combos = filter(lambda c: sum(c) == maxsum, combinations(packages, left_count))
  #       if not any(left_combos):
  #         continue
  #       for l in left_combos:
  #         rpackages = sorted(list(set(lpackages).difference(set(l))))
  #         for right_count in range(1, len(rpackages)):
  #           right_combos = filter(lambda c: sum(c) == maxsum, combinations(packages, right_count))
  #           if not any(right_combos):
  #             continue
  #           lowest_qe = min(lowest_qe, reduce(lambda x, y: x*y, f, 1))


if __name__ == '__main__':
  # x=Run('input/24t.txt')
  # assert x == 99, x
  # print("----")
  # print(Run('input/24.txt'))
  x=Run2('input/24t.txt')
  assert x == 44, x
  print("----")
  print(Run2('input/24.txt'))  