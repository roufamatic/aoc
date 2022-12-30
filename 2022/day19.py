import os
from parse import parse
from copy import deepcopy
from functools import cache
from collections import deque
from queue import LifoQueue, Empty
from random import random
from time import perf_counter, sleep, time
from multiprocessing import Pool, Lock, Value
from multiprocessing.managers import BaseManager
from datetime import timedelta

# Warning!
# this is some hideous multiprocessing (MP) code!
# * first time doing MP in python
# * no MP-compatible LIFO queue
# * didn't bother with locking because it massively slowed things down
# * zero tuning whatsoever
# * but it finishes part 1 in a couple minutes and part 2 in an hour.
# also probably some unused code from earlier attempts in here
# and I have zero intention of cleaning anything up!

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

class Blueprint:
  def __init__(self, line):
    (
        self.num, 
        self.orecost, 
        self.clayorecost, 
        self.obsorecost, 
        self.obsclaycost, 
        self.geoorecost, 
        self.geoobscost
    ) = parse('Blueprint {:d}: Each ore robot costs {:d} ore. Each clay robot costs {:d} ore. Each obsidian robot costs {:d} ore and {:d} clay. Each geode robot costs {:d} ore and {:d} obsidian.', line)
    self.line = line

    self.orebots = 1
    self.claybots = 0
    self.obsbots = 0
    self.geobots = 0

    self.ore = 0
    self.clay = 0
    self.obsidian = 0
    self.geodes = 0

    self.timePassed = 0
    self.skip = (False, False, False)
    self.history = []

  def PassTime(self, couldBuyObsBot = False, couldBuyClayBot = False, couldBuyOreBot = False):
    o = deepcopy(self)
    o.history.append([o.timePassed + 1, o.ore, o.clay, o.obsidian, o.geodes, o.skip, 'before'])
    o.ore += o.orebots
    o.clay += o.claybots
    o.obsidian += o.obsbots
    o.geodes += o.geobots
    o.skip = (couldBuyOreBot, couldBuyClayBot, couldBuyObsBot)
    o.timePassed += 1
    #o.history.append([o.timePassed, o.ore, o.clay, o.obsidian, o.geodes, o.skip, 'waited'])
    return o

  def CanBuyAnything(self) -> bool:
    return self.CanBuyOreBot() or self.CanBuyClayBot() or self.CanBuyObsidianBot() or self.CanBuyGeodeBot()

  def CanBuyOreBot(self) -> bool:
    if self.skip[0]: return False
    if self.orebots == max(self.clayorecost, self.obsorecost, self.geoorecost): return False
    return self.ore >= self.orecost

  def BuyOreBot(self):
    assert self.CanBuyOreBot()
    o = self.PassTime() 
    o.ore -= o.orecost
    o.orebots += 1
    #o.history[-1] = [o.timePassed, o.ore, o.clay, o.obsidian, o.geodes, o.skip, 'bought orebot']
    return o

  def CanBuyClayBot(self) -> bool:
    if self.skip[1]: return False
    if self.claybots == self.obsclaycost: return False
    return self.ore >= self.clayorecost

  def BuyClayBot(self):
    assert self.CanBuyClayBot()
    o = self.PassTime()
    o.ore -= o.clayorecost
    o.claybots += 1
    #o.history[-1] = [o.timePassed, o.ore, o.clay, o.obsidian, o.geodes, o.skip, 'bought claybot']
    return o

  def CanBuyObsidianBot(self) -> bool:
    if self.skip[2]: return False
    if self.obsbots == self.geoobscost: return False
    return self.ore >= self.obsorecost and self.clay >= self.obsclaycost

  def BuyObsidianBot(self):
    assert self.CanBuyObsidianBot()
    o = self.PassTime()
    o.ore -= o.obsorecost
    o.clay -= o.obsclaycost
    o.obsbots += 1
    # o.history[-1] = [o.timePassed, o.ore, o.clay, o.obsidian, o.geodes, o.skip, 'bought obsidianbot']
    return o

  def CanBuyGeodeBot(self) -> bool:
    return self.ore >= self.geoorecost and self.obsidian >= self.geoobscost

  def BuyGeodeBot(self):
    assert self.CanBuyGeodeBot()
    o = self.PassTime()
    o.ore -= self.geoorecost
    o.obsidian -= self.geoobscost
    o.geobots += 1
    #o.history[-1] = [o.timePassed, o.ore, o.clay, o.obsidian, o.geodes, o.skip, 'bought geodebot']
    return o

  def PrintHistory(self):
    for h in self.history:
      print(f'time={h[0]}, resources=[{h[1]}, {h[2]}, {h[3]}, {h[4]}], skip={h[5]}, op={h[6]}')

  @classmethod
  @cache
  def BpHash(cls, orb, cb, obb, gb):
    return (orb, cb, obb, gb).__hash__()

  def __hash__(self) -> int:
    return Blueprint.BpHash(self.orebots,self.claybots,self.obsbots,self.geobots)

########

materialgain = [0]
for i in range(1,34):
  materialgain.append(materialgain[i-1] + i)
@cache
def GetGain(time: int) -> int:
  global materialgain
  return sum(materialgain[0:time])

def Go(bp:Blueprint, t:int = 24, best:int=0):
  if bp.timePassed == t:
    return [None]
  
  possibleGeodes = bp.geodes + (bp.geobots * (t+1-bp.timePassed)) + GetGain(t+1-bp.timePassed)
  if possibleGeodes <= best:
    return [None]

  opts = []
  if bp.timePassed < t and bp.CanBuyGeodeBot():
    opts.append(bp.BuyGeodeBot())
  if bp.timePassed < t-2 and bp.CanBuyObsidianBot():
    opts.append(bp.BuyObsidianBot())
  if bp.timePassed < t-4 and bp.CanBuyClayBot():
    opts.append(bp.BuyClayBot())
  if bp.timePassed < t-3 and bp.CanBuyOreBot():
    opts.append(bp.BuyOreBot())
  opts.append(bp.PassTime(bp.CanBuyObsidianBot() or bp.skip[2], bp.CanBuyClayBot() or bp.skip[1], bp.CanBuyOreBot() or bp.skip[0]))
  return opts

class MyManager(BaseManager):
  pass 
MyManager.register('LifoQueue', LifoQueue)

def queue_muncher(q:LifoQueue,t:int):
  fails:int = 0
  start_time = time()
  while True:
    input:Blueprint = None
 #   with qlock:
    try:
      input = q.get_nowait()
    except Empty:
      fails += 1
    if fails > 0:
      print('nothing to do!')
      #sleep(random())
      #continue
      return global_best.value

    fails = 0
    if input:
      output = reversed(Go(input, t=t, best=global_best.value))
      for o in output: # q is a stack; put the juiciest result on top.
        if o and o.timePassed == t:
          if o.geodes > global_best.value:
            with global_best.get_lock():
              if o.geodes > global_best.value:
                global_best.value = o.geodes
                print(f'my new best = {global_best.value}')
        else:
#          with qlock:
          q.put_nowait(o)
    #with munch_counter.get_lock():
    munch_counter.value += 1
    if munch_counter.value % 100000 == 0:
      td = timedelta(seconds = time() - start_time)
      print(f'munched: {munch_counter.value}, best = {global_best.value}, time={td}')


def init_pool_processes(the_lock, the_munch_counter, the_best):
  '''Initialize each process with a global variable lock.
  '''
  global qlock, munch_counter, global_best
  qlock = the_lock
  munch_counter = the_munch_counter
  global_best = the_best


def Run(path):
  total = 0
  for l in ReadFile(path).splitlines():
    best = 0
    with MyManager() as mgr:
      munched = Value('i', 0)
      gbest = Value('i', 0)
      q:LifoQueue = mgr.LifoQueue()
      bp = Blueprint(l)
      q.put(bp)
      # create the shared lock
      lock = Lock()
      # Divide the work among two processes, storing partial results in sl
      with Pool(initializer=init_pool_processes, initargs=(lock,munched,gbest), processes=os.cpu_count()) as pool:
        results = [pool.apply_async(queue_muncher, (q,24)) for _ in range(os.cpu_count())]
        best = max([r.get() for r in results])
        print(f'best = {best}')
        total += (best * bp.num)
    print(f'{bp.num}: best = {best}')

  print(f'total={total}')  

def Run2(path):
  total = 1
  for l in ReadFile(path).splitlines()[0:3]:
    best = 0
    with MyManager() as mgr:
      munched = Value('i', 0)
      gbest = Value('i', 0)
      q:LifoQueue = mgr.LifoQueue()
      q.put(Blueprint(l))
      # create the shared lock
      lock = Lock()
      # Divide the work among two processes, storing partial results in sl
      with Pool(initializer=init_pool_processes, initargs=(lock,munched,gbest), processes=os.cpu_count()) as pool:
        results = [pool.apply_async(queue_muncher, (q,32)) for _ in range(os.cpu_count())]
        best = max([r.get() for r in results])
        print(f'best = {best}')
        total *= best

  print(f'total={total}')  


if __name__ == '__main__':
  #Run("input/19t.txt")
  #print("--------")
  Run("input/19.txt")

  #Run2("input/19t.txt")
  #print("--------")
  Run2("input/19.txt")

