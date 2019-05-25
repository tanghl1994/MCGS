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
    print('1')













        

