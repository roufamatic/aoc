import os

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)

  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Score(them, me):
  sv = {'X': 1, 'Y': 2, 'Z': 3}
  
  if them == 'A':
    if me == 'X':
      return 3 + sv[me]
    if me == 'Y':
      return 6 + sv[me]
    return 0 + sv[me]
  if them == 'B':
    if me == 'X':
      return 0 + sv[me]
    if me == 'Y':
      return 3 + sv[me]
    return 6 + sv[me]
  if them == 'C':
    if me == 'X':
      return 6 + sv[me]
    if me == 'Y':
      return 0 + sv[me]
    return 3 + sv[me]



def Score2(them, goal):
  adder = 0 if goal == 'X' else 3 if goal == 'Y' else 6
  sv = {'A': 1, 'B': 2, 'C': 3}
  if them == 'A':
    if goal == 'X': # lose: scissors
      return adder + sv['C']
    if goal == 'Y':
      return adder + sv['A']
    return adder + sv['B']

  if them == 'B':
    if goal == 'X': # lose: rock
      return adder + sv['A']
    if goal == 'Y':
      return adder + sv['B']
    return adder + sv['C']

  if them == 'C':
    if goal == 'X': # lose: rock
      return adder + sv['B']
    if goal == 'Y':
      return adder + sv['C']
    return adder + sv['A']

def Run(path):
  input = ReadFile(path)
  score = 0
  rounds = input.split('\n')
  for round in rounds:
    vals = round.split(' ')
    score += Score(vals[0], vals[1])
  print('part 1 = ' + str(score))

  score = 0
  for round in rounds:
    vals = round.split(' ')
    score += Score2(vals[0], vals[1])
  print('part 2 = ' + str(score))





Run("input/02t.txt")
print("--------")
Run("input/02.txt")
