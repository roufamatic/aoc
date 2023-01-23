def Say(numstr):
  d = None
  ct = 0
  rez = []
  for c in numstr:
    if d is None:
      d = c
      ct = 1
    elif d != c:
      rez.append(f'{ct}{d}')
      d = c
      ct = 1
    else:
      ct += 1
  rez.append(f'{ct}{c}')
  return ''.join(rez)

def Run():
  assert(Say('111221') == '312211')
  said = '3113322113'
  for i in range(40):
    said = Say(said)
  print(len(said))
  said = '3113322113'
  for i in range(50):
    said = Say(said)
  print(len(said))

if __name__ == '__main__':
  Run()