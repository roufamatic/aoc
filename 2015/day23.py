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

def Inc(registers, reg):
  def output():
    registers[reg] += 1
    return 1
  return output

def Hlf(registers, reg):
  def output():
    registers[reg] //= 2
    return 1
  return output

def Tpl(registers, reg):
  def output():
    registers[reg] *= 3
    return 1
  return output

def Jmp(next):
  def output():
    return next
  return output

def Jie(registers, reg, next):
  def output():
    return next if registers[reg] % 2 == 0 else 1
  return output

def Jio(registers, reg, next):
  def output():
    return next if registers[reg] == 1 else 1
  return output

def Run(path, aval = 0):
  instrux = []
  registers = {'a':aval, 'b':0}
  for line in ReadFile(path).splitlines():
    if line.startswith('inc'):
      instrux.append(Inc(registers, line.split(' ')[1]))
    elif line.startswith('hlf'):
      instrux.append(Hlf(registers, line.split(' ')[1]))
    elif line.startswith('tpl'):
      instrux.append(Tpl(registers, line.split(' ')[1]))
    elif line.startswith('jmp'):
      instrux.append(Jmp(int(line.split(' ')[1])))
    elif line.startswith('jie'):
      (reg, val) = parse('jie {}, {:d}', line)
      instrux.append(Jie(registers, reg, val))
    elif line.startswith('jio'):
      (reg, val) = parse('jio {}, {:d}', line)
      instrux.append(Jio(registers, reg, val))
    else:
      assert False, 'huh?'

  ptr = 0
  while ptr < len(instrux):
    ptr += instrux[ptr]()
  
  print(registers['b'])

if __name__ == '__main__':
  Run('input/23.txt')
  Run('input/23.txt', 1)

