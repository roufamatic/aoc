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
  dirs = {'^':(0,-1), '>': (1,0), 'v': (0,1), '<': (-1,0)}
  pos = (0,0)
  visited = set([pos])
  for c in ReadFile(path):
    pos = (pos[0] + dirs[c][0], pos[1] + dirs[c][1])
    visited.add(pos)

  print(len(visited))
  
  pos = [(0,0), (0,0)]
  visited = set([pos[0]])
  for ix, c in enumerate(ReadFile(path)):
    i = ix % 2
    pos[i] = (pos[i][0] + dirs[c][0], pos[i][1] + dirs[c][1])
    visited.add(pos[i])
  
  print(len(visited))


if __name__ == '__main__':
  Run('input/03.txt')
