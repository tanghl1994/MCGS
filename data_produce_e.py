import random

a = [random.random() for i in range(11)]
print(57)
print('1,2,3,4,5')
m = 6
for i in range(6):
    for j in range(i+5):
        print('%d,%d' % (m,m+1))
        m += 1
    m += 1

for i in range(11):
    print()


for i in range(6):
    for j in range(i+5):
        if i%2 == 0:
            print('min')
        else:
            print('max')

for i in range(11):
    print(a[i])

for i in range(11):
    print('random')




print(636)
print('1,2,3,4,5')
n = 5
m = 6
for i in range(6):
    for j in range(n):
        print('%d,%d' % (m,m+1))
        m = m + 2
    n = n * 2
for i in range(320):
    print()

n=5
for i in range(6):
    for j in range(n):
        if i%2==0:
            print('min')
        else:
            print('max')

    n = n*2

b = [0,0,0,0,0,0]
i = 0
j = 0
while j < 320:
    while i!=6:
        if i != 0:
            if b[i] == 2:
                b[i] = 0
                i = i - 1
                b[i] = b[i] + 1
                continue
            else:
                i = i + 1
                continue
        else:
            i = i + 1
            continue

    print(a[sum(b)])
    print(a[sum(b)+1])
    i = 5
    b[i] = b[i] + 1
    j = j + 2
for i in range(320):
    print('random')
    
                
        
        











        

