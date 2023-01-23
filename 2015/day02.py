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
  area = 0
  ribbon = 0
  for r in ReadFile(path).splitlines():
    l,w,h = [int(v) for v in r.split('x')]
    s = sorted([l, w, h])
    s1 = l*w
    s2 = w*h
    s3 = l*h
    area += 2 * s1 + 2 * s2 + 2 * s3 + (s[0] * s[1])

    ribbon += (2 * s[0] + 2 * s[1]) + (l * w * h)


  print(f'paper: {area}')
  print(f'ribbon: {ribbon}')


if __name__ == '__main__':
  Run('input/02t.txt')
  print('-----')
  Run('input/02.txt')
