import random
print(111)
for i in range(9):
    print(i+1,end=',')
print(10)

for i in range(10):
    for j in range(9):
        print((i+1)*10+j+1,end=',')
    print((i+2)*10)

for i in range(100):
    print()

for i in range(10):
    print('min')

for i in range(100):
    a = random.random()
    while (a==0):
        a = random.random()
    print(a)

for i in range(100):
    print('random')    
