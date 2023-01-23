from hashlib import md5

def Run():
  input = 'bgvyzdsv'
  
  i = 0
  found = False
  while True:
    check = input + str(i)
    res = md5(check.encode('utf-8')).hexdigest()
    if res[:5] == '00000' and not found:
      found = True
      print(f'at {i}, {check}, {res}')
    if res[:6] == '000000':
      print(f'at {i}, {check}, {res}')
      return
    i += 1
    if i % 100000 == 0: print(f'still chugging... {i} (last res == {res})')

# 150398 is too low?
if __name__ == '__main__':
  Run()
