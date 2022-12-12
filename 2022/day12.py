import os

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def DisplayPath(path, lines):
  GREEN = '\033[92m'
  GREY = '\033[0m'

  for y, l in enumerate(lines):
    for x, c in enumerate(l):
      if (x, y) in path:
        print(f'{GREEN}{c}{GREY}', end = '')
      else:
        print(c, end='')
    print()


def Run(path, hike = False):
  input = ReadFile(path)
  lines = [v.strip() for v in input.split('\n')]
  positions = {}
  startpos = []
  endpos = None
  for y, l in enumerate(lines):
    for x, c in enumerate(l):
      if c == 'E':
        endpos = (x,y)
        positions[(x,y)] = ord('z')  
      else:
        positions[(x,y)] = ord(c)
      
      if (hike and c in ['a', 'S']) or (not hike and c == 'S'):
        startpos.append((x,y))
      
  assert startpos
  visited = set(startpos)

  queue = []

  for p in startpos:
    queue.extend([
      (p[0] - 1, p[1], [(p[0] - 1, p[1])], ord('a')),
      (p[0] + 1, p[1], [(p[0] + 1, p[1])], ord('a')),
      (p[0], p[1] - 1, [(p[0], p[1] - 1)], ord('a')),
      (p[0], p[1] + 1, [(p[0], p[1] + 1)], ord('a'))])

  while len(queue) > 0:
    (x, y, path, oldheight) = queue.pop()
    
    if (x, y) not in positions:
      continue
    
    if (x,y) == endpos:
      print(len(path))
      DisplayPath(path, lines)
      break

    if positions[(x,y)] <= oldheight + 1:
      if (x, y) in visited:
        continue

      visited.add((x, y))

      for v in [
        (x - 1, y, path + [(x - 1, y)], positions[(x,y)]),
        (x + 1, y, path + [(x + 1, y)], positions[(x,y)]),
        (x, y - 1, path + [(x, y - 1)], positions[(x,y)]),
        (x, y + 1, path + [(x, y + 1)], positions[(x,y)]),
      ]:
        queue.insert(0, v)


Run("input/12t.txt")
print("--------")
Run("input/12.txt")

Run("input/12t.txt", True)
print("--------")
Run("input/12.txt", True)

