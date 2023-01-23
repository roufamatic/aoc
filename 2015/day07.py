import os
from parse import search
from copy import deepcopy
from collections import defaultdict
from frozendict import frozendict
from functools import cache

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

@cache
def GetVal(d, v):
  if v in d:
    return d[v](d)
  else:
    return int(v)

ops = {
  'AND': lambda d,a,b: GetVal(d, a) & GetVal(d, b),
  'OR': lambda d,a,b: GetVal(d, a) | GetVal(d, b),
  'NOT': lambda d,a: ~GetVal(d,a),
  'LSHIFT': lambda d,a,b: GetVal(d,a) << GetVal(d,b),
  'RSHIFT': lambda d,a,b: GetVal(d,a) >> GetVal(d,b),
  'EQ': lambda d,a: GetVal(d,a)
  } 

def Run(path):
  vals = {}
  for l in ReadFile(path).splitlines():
    bits = l.split(' -> ')
    var = bits[1]
    args = bits[0].split(' ')
    assert var not in vals
    if len(args) == 1:
      vals[var] = lambda d,args=args: GetVal(d, args[0])
    elif len(args) == 2:
      assert args[0] == 'NOT'
      vals[var] = lambda d,args=args: ops['NOT'](d, args[1])
    else:
      assert len(args) == 3 and args[1] in ops
      vals[var] = lambda d,args=args: ops[args[1]](d, args[0], args[2])

  fd = frozendict(vals)
  print(GetVal(fd, 'a'))

  GetVal.cache_clear()
  vals['b'] = lambda d: 956
  fd = frozendict(vals)
  print(GetVal(fd, 'a'))


if __name__ == '__main__':
  Run('input/07.txt')
  
