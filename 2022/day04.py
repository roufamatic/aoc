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


Run("input04t.txt")
print("--------")
Run("input04.txt")
