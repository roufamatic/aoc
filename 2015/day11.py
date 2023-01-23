
def Increment(p):
  plen = len(p)
  l = list(p)
  foundillicit = False
  for ix in range(plen):
    if foundillicit:
      l[ix] = 'a'
    else:
      c = l[ix]
      if c in 'iol':
        l[ix] = chr(ord(c) + 1)
        foundillicit = True

  p = list(reversed(l))
  while True:
    rez = []
    for ix,c in enumerate(p):
      v = ord(c) + 1 
      if v > ord('z'):
        rez.append('a')
      else:
        if chr(v) in 'iol':
          rez.append(chr(v + 1))
        else:
          rez.append(chr(v))
        break
    if len(rez) < plen:
      rez.extend(p[ix + 1:])
    
    firstdouble = -1
    founddoubles = False
    foundrun = False
    for ix in range(len(rez)):
      c = rez[ix]
      if ix > 0 and rez[ix-1] == rez[ix]:
        if firstdouble == -1:
          firstdouble = ix
        elif ix - 1 != firstdouble:
          founddoubles = True
      if ix > 1 and ord(rez[ix]) + 1 == ord(rez[ix - 1]) and ord(rez[ix]) + 2 == ord(rez[ix - 2]):
        foundrun = True
    if founddoubles and foundrun:
      return ''.join(reversed(rez))
    p = ''.join(rez)


def Run():
  t1 = Increment('abcdefgh')
  assert t1 == 'abcdffaa', f'wanted abcdffaa, got {t1}'
  t2 = Increment('ghijklmn')
  assert t2 == 'ghjaabcc', f'wanted ghjaabcc, got {t2}'
  print(Increment('hepxcrrq'))
  print(Increment(Increment('hepxcrrq')))



if __name__ == '__main__':
  Run()