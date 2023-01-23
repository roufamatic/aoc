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

def Run(path):
  l = ReadFile(path)
  d = {'(': 1, ')': -1}
  print(sum([d[c] for c in l]))

  v = 0
  for ix, c in enumerate(l):
    v += d[c]
    if v == -1:
      print(ix + 1)
      return

if __name__ == '__main__':
  #Run('01t.txt')
  #print('-----')
  Run('input/01.txt')
