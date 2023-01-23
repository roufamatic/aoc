from __future__ import annotations
import math
from itertools import combinations

class Character():
  def __init__(self, hp, cost, damage, armor) -> None:
    self.hp = hp
    (self.cost, self.damage, self.armor) = (cost,damage,armor)

  def Defeats(self, other: Character):
    mydeath = math.ceil(self.hp / max(other.damage - self.armor, 1))
    theirdeath = math.ceil(other.hp / max(self.damage - other.armor, 1))
    return mydeath >= theirdeath

def Run():
  weapons = [(8,4,0),(10,5,0),(25,6,0),(40,7,0),(74,8,0)]
  armor = [(0,0,0),(13,0,1),(31,0,2),(53,0,3),(75,0,4),(102,0,5)]
  rings = [(0,0,0),(0,0,0),(25,1,0),(50,2,0),(100,3,0),(20,0,1),(40,0,2),(80,0,3)]

  enemy = Character(104, 0, 8, 1)

  best = math.inf
  worst = 0
  for w in weapons:
    for a in armor:
      for r in combinations(rings, 2):
        stuff = list(r)
        stuff.extend([w,a])
        vals = tuple([sum(z) for z in zip(*stuff)])
        char = Character(100, vals[0],vals[1],vals[2])
        if char.Defeats(enemy) and char.cost < best:
          best = char.cost
        elif enemy.Defeats(char) and char.cost > worst:
          worst = char.cost
  print(f'best: {best}, worst: {worst}')

if __name__ == '__main__':
  Run()