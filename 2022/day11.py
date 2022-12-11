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

class Monkey:
  def __init__(self, relief):
    self.items = []
    self.fn = None
    self.test = 0
    self.throwTrue = -1
    self.throwFalse = -1
    self.inspections = 0
    self.relief = relief

  def InspectAndThrow(self, monkeys, testprod):
    for item in self.items:
      item = self.fn(item)
      item = item // self.relief
      item = item % testprod
      if item % self.test == 0:
        monkeys[self.throwTrue].items.append(item)
      else:
        monkeys[self.throwFalse].items.append(item)
      self.inspections += 1
    self.items = []
  
  def SetFn(self, fn):
    self.fn = fn

def Run(path, relief, rounds):
  input = ReadFile(path)
  lines = [v.strip() for v in input.split('\n')]
  
  monkeys = []
  monkey = None
  for line in lines:
    if parse('Monkey {:d}:', line):
      monkey = Monkey(relief)
      monkeys.append(monkey)
      continue
    
    itemstr = parse('Starting items: {}', line)
    if itemstr:
      monkey.items.extend([int(v) for v in itemstr[0].split(', ')])
      continue

    operation = parse('Operation: {}', line)
    if operation:
      if '*' in line:
        arg = line.split('* ')[1]
        if arg == 'old':
          monkey.SetFn(lambda old, arg=arg: old * old)
        else:
          monkey.SetFn(lambda old, arg=arg: old * int(arg))
      if '+' in line:
        arg = line.split('+ ')[1]
        if arg == 'old':
          monkey.SetFn(lambda old, arg=arg: old + old)
        else:
          monkey.SetFn(lambda old, arg=arg: old + int(arg))

      assert monkey.fn, 'no function!'
      continue

    test = parse('Test: divisible by {:d}', line)
    if test:
      monkey.test = test[0]
      continue

    throwTrue = parse('If true: throw to monkey {:d}', line)
    if throwTrue:
      monkey.throwTrue = throwTrue[0]
      continue

    throwFalse = parse('If false: throw to monkey {:d}', line)
    if throwFalse:
      monkey.throwFalse = throwFalse[0]
      continue
  #####
  m = 1
  for monkey in monkeys:
    m *= monkey.test

  for i in range(rounds):
    for monkey in monkeys:
      monkey.InspectAndThrow(monkeys, m)

  best1 = 0
  best2 = 0
  for monkey in monkeys:
    if monkey.inspections > best1:
      best2 = best1
      best1 = monkey.inspections
    elif monkey.inspections > best2:
      best2 = monkey.inspections

  print(best1*best2)




Run("input/11t.txt", 3, 20)
print("--------")
Run("input/11.txt", 3, 20)

Run("input/11t.txt", 1, 10000)
print("--------")
Run("input/11.txt", 1, 10000)
