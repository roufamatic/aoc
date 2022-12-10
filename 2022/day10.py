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


class Device:
  def __init__(self):
    self.x = 1
    self.tick = 0
    self.strength = 0
    self.row = 0

  def CheckTick(self):
    
    # render
    pos = self.tick % 40
    if pos in range(self.x - 1, self.x + 2):
      print('#', end='')
    else:
      print('.', end='')

    self.tick+=1
    if self.tick in [20,60,100,140,180,220]:
      # print(f'{self.tick}: {self.x * self.tick}')
      self.strength += (self.tick * self.x)

    if self.tick in [40, 80, 120, 160, 200]:
      print()


  def Noop(self):
    self.CheckTick()

  def Add(self, val):
    self.CheckTick()
    self.CheckTick()
    self.x += val


def Run(path):
  input = ReadFile(path)
  lines = [v.strip() for v in input.split('\n')]
  
  device = Device()

  for line in lines:
    if line == 'noop':
      device.Noop()
    else:
      val = parse('addx {:d}', line)[0]
      device.Add(val)
  print()
  print(device.strength)


Run("input/10t.txt")
print("--------")
Run("input/10.txt")

