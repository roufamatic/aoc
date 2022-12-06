import os

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)

  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Run(path):
  input = ReadFile(path)
  lines = [v.strip() for v in input.split('\n')]
  total = 0
  for line in lines:
    (r1, r2) = line.split(',')
    (l1, h1) = [int(v) for v in r1.split('-')]
    (l2, h2) = [int(v) for v in r2.split('-')]
    if (l1 <= l2 and h1 >= h2) or (l2 <= l1 and h2 >= h1):
      total += 1
  print(total)

  total = 0
  for line in lines:
    (r1, r2) = line.split(',')
    (l1, h1) = [int(v) for v in r1.split('-')]
    (l2, h2) = [int(v) for v in r2.split('-')]
    
    rr1 = set(range(l1, h1 + 1))
    rr2 = set(range(l2, h2 + 1))
    if len(rr1.intersection(rr2)) > 0:
      total += 1
    
  print(total)


Run("input/04t.txt")
print("--------")
Run("input/04.txt")
