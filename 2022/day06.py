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
  line = lines[0]
  arr = []
  for ix, c in enumerate(line):
    arr.insert(0, c)
    if len(arr) > 4:
      arr.pop()
      if len(set(arr)) == 4:
        print(ix + 1)
        break
  arr = []
  for ix, c in enumerate(line):
    arr.insert(0, c)
    if len(arr) > 14:
      arr.pop()
      if len(set(arr)) == 14:
        print(ix + 1)
        return




Run("input06t.txt")
print("--------")
Run("input06.txt")
