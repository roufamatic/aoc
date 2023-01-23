import math
from functools import cache
from sympy import divisors

def Run():
  goal = 33100000 / 10
  steps = 1 
  while True:
    if steps % 10000 == 0:
      print(f'steps: {steps}')
    f = divisors(steps)
    r = sum(f)
    if r >= goal:
      print(f'answer={steps}')
      break
    steps += 1

  # part 2
  output = [0] * 100000000
  i = 0
  best = math.inf
  while True:
    i += 1
    for s in range(1, 51):
      house = i * s
      if house >= len(output): 
        print(f'answer 2 = {best}')
        return
      output[house] += (11 * i)
      if output[house] >= 33100000:
        if house < best:
          print(f'new best = {house}')
          best = house


if __name__ == '__main__':
  Run()