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

def manhattan(p1, p2):
  return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def Run(path, row):
  input = [((p[0], p[1]),(p[2], p[3])) for p in [parse('Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}', l) for l in ReadFile(path).split('\n')]]
  allbeacons = set([p[1] for p in input])
  maxmd = max([manhattan(sensor,beacon) for sensor,beacon in input])

  minx = min([p[1][0] for p in input]) - maxmd
  maxx = max([p[1][0] for p in input]) + maxmd
  print(f'minx={minx}, maxx={maxx}')

  takeninrow = set()
  for (sensor, beacon) in input:
    sbmanhattan = manhattan(sensor, beacon)
    for i in range(minx, maxx+1):
      p = (i, row)
      if p not in allbeacons and manhattan(p, sensor) <= sbmanhattan:
        takeninrow.add(p)

  print(len(takeninrow))

def GetPointsWithMD(sensor, dist, maxc):
  for x in range(dist + 1):
    # d = 0: only add two points (top and bottom)
    # d > 0: add four points
    
    def ok(p):
      return p[0] >= 0 and p[0] <= maxc and p[1] >= 0 and p[1] <= maxc

    if x == 0:
      for p in [(sensor[0], sensor[1]-dist), (sensor[0], sensor[1]+dist)]:
        if ok(p): yield(p)
    elif x == dist:
      for p in [(sensor[0]-dist, sensor[1]),(sensor[0]+dist, sensor[1])]:
        if ok(p): yield(p)
    else:
      for p in [(sensor[0]-x, sensor[1]-(dist-x)),(sensor[0]-x, sensor[1]+(dist-x)),(sensor[0]+x, sensor[1]-(dist-x)),(sensor[0]+x, sensor[1]+(dist-x))]:
        if ok(p): yield(p)


def Run2(path, maxc):
  input = [((p[0], p[1]),(p[2], p[3])) for p in [parse('Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}', l) for l in ReadFile(path).split('\n')]]
  allbeacons = set([p[1] for p in input])

  def within(point):
    for (sensor, beacon) in input:
      if manhattan(sensor, point) <= manhattan(sensor, beacon):
        return True
    return False
  i = 0
  for (sensor, beacon) in input:
    i += 1
    print(f'{i}. {sensor} - {beacon}')
    md = manhattan(sensor, beacon)
    # limit the possibilities to those points that are just outside each sensor's range.
    for p in GetPointsWithMD(sensor, md + 1, maxc):
      if not within(p):
        print(p[0] * 4000000 + p[1])
        return

Run("input/15t.txt", 10)
Run2("input/15t.txt", 20)
print("--------")
Run("input/15.txt", 2000000)
Run2("input/15.txt", 4000000)
