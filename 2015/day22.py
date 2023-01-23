from __future__ import annotations
from copy import deepcopy
import heapq

class Turn:
  def __init__(self, turn: Turn = None):
    if turn == None:
      self.boss_hp = 58
      self.boss_dmg = 9
      self.mana = 500
      self.hp = 50
      self.spent_mana = 0
      self.armor = 0
      self.active_spells = []
      self.used_spells = []
    else:
      self.boss_hp = turn.boss_hp
      self.boss_dmg = turn.boss_dmg
      self.mana = turn.mana
      self.hp = turn.hp
      self.spent_mana = turn.spent_mana
      self.armor = turn.armor
      self.active_spells = deepcopy(turn.active_spells)
      self.used_spells = deepcopy(turn.used_spells)
  
  def __lt__(self, other: Turn):
    return self.spent_mana < other.spent_mana

  def Cast(self, spell):
    (time, cost, damage, armor, heal, mana) = spell
    self.used_spells.append(spell)
    self.mana -= cost
    self.spent_mana += cost
    self.armor += armor
    if time == 0:
      self.hp += heal
      self.boss_hp -= damage
    else:
      self.active_spells.append(spell)

  def Defend(self):
    self.hp -= max(1, self.boss_dmg - self.armor)

  def Tick(self):
    myspells = deepcopy(self.active_spells)
    self.active_spells.clear()
    while myspells:
      (time, cost, damage, armor, heal, mana) = myspells.pop()
      assert time > 0
      time -= 1
      self.boss_hp -= damage
      self.hp += heal
      self.mana += mana
      if time <= 0:
        # armor expires
        self.armor -= armor
        continue
      self.active_spells.append((time, cost, damage, armor, heal, mana))

  def Dead(self):
    return self.hp <= 0

  def BossDefeated(self):
    return self.boss_hp <= 0

def GetSpells():
  # time, cost, damage, armor, heal, mana
  yield (0, 53, 4, 0, 0, 0) # magic missile
  yield (0, 73, 2, 0, 2, 0) # drain
  yield (6, 113, 0, 7, 0, 0) # shield
  yield (6, 173, 3, 0, 0, 0) # poison
  yield (5, 229, 0, 0, 0, 101) # recharge

def Run(hard = False):
  pq:list[Turn] = [Turn()]
  while len(pq) > 0:
    turn: Turn = heapq.heappop(pq)
    if turn.BossDefeated():
      print(turn.spent_mana)
      print(turn.used_spells)
      return
    if hard:
      turn.hp -= 1
      if turn.Dead():
        continue
    turn.Tick()
    if turn.BossDefeated():
      print(turn.spent_mana)
      print(turn.used_spells)
      return
    for s in GetSpells():
      if turn.mana < s[1]:
        continue
      if any(filter(lambda acts: acts[1] == s[1], turn.active_spells)):
        continue
      t = Turn(turn)
      t.Cast(s)
      t.Tick()
      if not t.BossDefeated():
        t.Defend()
      if not t.Dead():
        heapq.heappush(pq, t)

              
    


if __name__ == '__main__':
  #241 is too low
  Run()
  Run(True)