import os
from parse import parse
from copy import deepcopy

def ReadFile(path):
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  path = os.path.join(__location__, path)
  tf = open(path, "r")
  output = tf.read()
  tf.close()
  return output

def Diag(arr):
  a = deepcopy(arr)
  for i in range(0, len(a)):
    for j in range(i+1, len(a[0])):
      a[i][j],a[j][i] = a[j][i],a[i][j]
  return a

def Run(path):
  input = ReadFile(path)
  lines = [v.strip() for v in input.split('\n')]
  arr = []
  for line in lines:
    inner = [int(v) for v in line]
    arr.append(inner)
  
  height = len(arr)
  width = len(arr[0])
  total = 2 * height + 2 * width - 4

  darr = Diag(arr)
  #print(darr)
  for rix in range(1, height - 1):
    for cix in range(1, width - 1):
      v = arr[rix][cix]
      maxl = max(arr[rix][0:cix])
      maxr = max(arr[rix][cix+1:width])
      maxu = max(darr[cix][0:rix])
      maxd = max(darr[cix][rix+1:height])

      #print(f'checking ({rix},{cix})={v}: {maxl},{maxr},{maxu},{maxd}')

      if maxl < v or maxr < v or maxu < v or maxd < v: 
        total+=1
  print(total)

  best = 1
  for rix in range(1, height - 1):
    for cix in range(1, width - 1):
      v = arr[rix][cix]
      mm = 1

      m = 0
      for ccix in range(cix-1, -1, -1):
        t = arr[rix][ccix]
        m += 1
        if t >= v:
          break
      mm *= m

      m = 0
      for ccix in range(cix+1, width):
        t = arr[rix][ccix]
        m += 1
        if t >= v:
          break
      mm *= m

      m = 0
      for rrix in range(rix-1, -1, -1):
        t = arr[rrix][cix]
        m += 1
        if t >= v:
          break
      mm *= m

      m = 0
      for rrix in range(rix+1, height):
        t = arr[rrix][cix]
        m += 1
        if t >= v:
          break
      mm *= m

      if mm > best: 
        best = mm

  print(best)
    
      







Run("input/08t.txt")
print("--------")
Run("input/08.txt")

