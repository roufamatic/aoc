import os
import re
from parse import parse
from copy import deepcopy

class Node:
  def __init__(self, valve, flow_rate, tunnels):
    self.open = False
    self.valve = valve
    self.flow_rate = flow_rate
    self.tunnels = set(tunnels)
    self.neighbors = {}

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output


def FindFlowingNeighbors(nodes, node, steps, visited, output):
  if steps > 0 and node.flow_rate > 0:
    output[node.valve] = steps
  elif node.valve not in visited:
    visited.add(node.valve)
    for n in node.tunnels:
      if n in visited: continue
      FindFlowingNeighbors(nodes, nodes[n], steps+1, deepcopy(visited), output)

def Explore(nodes, node, score, clock, openedValves, visitedSinceOpen, best = 0):
  if clock <= 0: 
    return max(score, best)

  ov = deepcopy(openedValves)
  vso = deepcopy(visitedSinceOpen)
  for n in node.neighbors:
    if n in visitedSinceOpen: continue
    vso.add(n)
    best = max(best, Explore(nodes, nodes[n], score, clock-node.neighbors[n], ov, vso, best))

  if node.valve not in openedValves and node.valve != 'AA':
    ov.add(node.valve)
    vso = set([node.valve])
    clock -= 1
    score += (node.flow_rate * clock)

    if clock <= 0:
      return max(score, best)

    for n in node.neighbors:
      vso.add(n)
      best = max(best, Explore(nodes, nodes[n], score, clock-node.neighbors[n], ov, vso, best))
  return best  

def Explore2(nodes, node, score, clock, openedValves, visitedSinceOpen, output):
  if clock <= 0:
    return
  if openedValves:
    output.add((score, frozenset(openedValves)))

  for n in node.neighbors:
    if n in visitedSinceOpen: continue
    vso = deepcopy(visitedSinceOpen)
    vso.add(n)
    Explore2(nodes, nodes[n], score, clock-node.neighbors[n], deepcopy(openedValves), vso, output)

  if node.valve not in openedValves and node.valve != 'AA':
    ov = deepcopy(openedValves)
    ov.add(node.valve)
    vso = set([node.valve])
    clock -= 1
    score += (node.flow_rate * clock)

    if clock <= 0:
      output.add((score, frozenset(openedValves)))
      return

    for n in node.neighbors:
      vso.add(n)
      Explore2(nodes, nodes[n], score, clock-node.neighbors[n], ov, vso, output)


def Run(path, elephant = False):
  input = ReadFile(path).split('\n')
  
  startnode = None
  nodes = {}
  
  for line in input:
    m = re.search('Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnels? leads? to valves? (.*)', line)
    
    node = Node(m.group(1), int(m.group(2)), m.group(3).split(', '))
    if node.valve == 'AA':
      startnode = node
    nodes[node.valve] = node

  flowers = {n.valve: n for n in filter(lambda n: n.flow_rate > 0, nodes.values())}
  #print(flowers)

  for node in flowers.values():
    FindFlowingNeighbors(nodes, node, 0, set(), node.neighbors)
  
  FindFlowingNeighbors(nodes, startnode, 0, set(), startnode.neighbors)
  opened = set()
  output = set()
  if elephant:
    Explore2(flowers, startnode, 0, 26, opened, set(['AA']), output)
    print(f'len(output)={len(output)}')
    best = 0
    outputlist = list(sorted(output, reverse=True))
    for ix, (score, ov) in enumerate(outputlist):
      for jx in range(ix + 1, len(outputlist)):
        (score2, ov2) = outputlist[jx]
        if ov & ov2:
          continue
        if score+score2 > best:
          best = score+score2
          print(best)
        if score+score2 < best/2:
          return
  else:
    print(Explore(flowers, startnode, 0, 30, opened, set(['AA'])))


Run("input/16t.txt")
print("--------")
Run("input/16.txt")
print("--------")
Run("input/16t.txt", True)
print("--------")
Run("input/16.txt", True)
