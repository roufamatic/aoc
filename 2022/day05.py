import copy
import os
import re

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)

  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Run(path, stacks_orig):
  stacks = copy.deepcopy(stacks_orig)
  print(stacks)

  input = ReadFile(path).split('\n\n')[1]
  lines = [v.strip() for v in input.split('\n')]
  
  for line in lines:
    match = re.search('^move (\d+) from (\d+) to (\d+)$', line)
    assert match
    numtomove = int(match.group(1))
    fromstack = int(match.group(2)) - 1
    tostack = int(match.group(3)) - 1

    for i in range(0, numtomove):
      stacks[tostack].append(stacks[fromstack].pop())
    
    print(stacks)
    print(stacks_orig)

  output = ''.join([s[len(s) - 1] for s in stacks])

  print('#####')

  stacks = copy.deepcopy(stacks_orig)
  for line in lines:
    match = re.search('^move (\d+) from (\d+) to (\d+)$', line)
    assert match
    numtomove = int(match.group(1))
    fromstack = int(match.group(2)) - 1
    tostack = int(match.group(3)) - 1

    tmp = []
    for i in range(0, numtomove):
      tmp.append(stacks[fromstack].pop())
    for i in range(0, numtomove):
      stacks[tostack].append(tmp.pop())

    print(stacks)

  output = ''.join([s[len(s) - 1] for s in stacks])

  print(output)


#     [D]    
# [N] [C]    
# [Z] [M] [P]
#  1   2   3 
sss = [['Z','N'], ['M','C','D'], ['P']]
Run('input05t.txt', sss)
print("--------")

sss = [list(v) for v in [
  'FTNZMGHJ',
  'JWV',
  'HTBJLVG',
  'LVDCNJPB',
  'GRPMSWF',
  'MVNBFCHG',
  'RMGHD',
  'DZVMNH',
  'HFNG']]

for s in sss:
  s.reverse()

#print(sss)


# [F]         [L]     [M]            
# [T]     [H] [V] [G] [V]            
# [N]     [T] [D] [R] [N]     [D]    
# [Z]     [B] [C] [P] [B] [R] [Z]    
# [M]     [J] [N] [M] [F] [M] [V] [H]
# [G] [J] [L] [J] [S] [C] [G] [M] [F]
# [H] [W] [V] [P] [W] [H] [H] [N] [N]
# [J] [V] [G] [B] [F] [G] [D] [H] [G]
#  1   2   3   4   5   6   7   8   9 




#Run('input05.txt', sss)