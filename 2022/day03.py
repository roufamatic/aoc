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
    c1 = line[0:len(line)//2]
    c2 = line[len(line)//2:]
    s = set()
    for c in c1:
      s.add(c)
    for c in c2:
      if c in s:
        if c.upper() == c:
          val = ord(c) - ord('A') + 27
        else:
          val = ord(c) - ord('a') + 1
        total += val
        break
  
  print(total)

  total = 0
  ix = 0
  while(ix < len(lines)):
    s = set(lines[ix])
    ix += 1
    s = s.intersection(set(lines[ix]))
    ix += 1
    s = s.intersection(set(lines[ix]))
    assert len(s) == 1
    c = s.pop()
    if c.upper() == c:
      val = ord(c) - ord('A') + 27
    else:
      val = ord(c) - ord('a') + 1
    total += val
    ix += 1
  print(total)



Run("input03t.txt")
print("--------")
Run("input03.txt")
