import random
print(13)
for i in range(2):
    print(i+1,end=',')
print(3)

for i in range(3):
    for j in range(2):
        print((i+1)*3+j+1,end=',')
    print((i+2)*3)

for i in range(9):
    print()

for i in range(3):
    print('min')

for i in range(9):
    a = random.random()
    while (a==0):
        a = random.random()
    print(a)

for i in range(9):
    print(1)    
