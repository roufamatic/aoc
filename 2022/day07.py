import os

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output


class PathNode:
  def __init__(self, name, parent):
    self.name = name
    self.parent = parent
    self.kids = []
    self.items = []

  def AddChild(self, node):
    self.kids.append(node)

  def MySize(self):
    sum = 0
    for k in self.kids:
      sum += k.MySize()
    for i in self.items:
      sum += i[1]
    return sum

def Find100KNodes(node):
  sum = 0
  if node.MySize() <= 100000:
    sum += node.MySize()
  for k in node.kids:
    sum += Find100KNodes(k)
  return sum

def FindBestNodeUnder(node, limit):
  # find the node that is bigger than limit but smaller than every other choice.
  best = 70000000
  mysize = node.MySize()
  if mysize < best and mysize >= limit:
    best = node.MySize()
  for k in node.kids:
    kb = FindBestNodeUnder(k, limit)
    if kb < best and kb >= limit:
      best = kb
  return best

def Run(path):
  input = ReadFile(path)
  lines = [v.strip() for v in input.split('\n')]
  firstnode = None
  curnode = None
  for line in lines:
    if line[0] == '$':
      cmd = line[2:]
      if cmd == 'ls':
        # This doesn't matter.
        assert curnode
        continue
      else:
        arg = cmd.split(' ')[1]
        if arg == '..':
          assert curnode
          curnode = curnode.parent
        else:
          newnode = PathNode(arg, curnode)
          if firstnode is None:
            firstnode = newnode
          if curnode is not None:
            curnode.AddChild(newnode)
          curnode = newnode
          
    else:
      if line.startswith('dir'):
        # I don't care about dir lines, only the ones we traverse afaict
        continue
      else:
        t = line.split(' ')
        item = (t[1], int(t[0]))
        curnode.items.append(item)
  
  print(Find100KNodes(firstnode))
  
  totalsize = firstnode.MySize()
  unused = 70000000 - totalsize
  needed = 30000000 - unused
  print(FindBestNodeUnder(firstnode, needed))


Run("input/07t.txt")
print("--------")
Run("input/07.txt")
