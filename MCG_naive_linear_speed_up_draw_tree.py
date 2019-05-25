import matplotlib.pyplot as plt



tree_max = 1200

a = 0.1
x = [1,4,16,64,256]


b = []
f_tree = open('final_linearly_speedup_result_MCG_tree.txt')
lines = f_tree.readlines()
line = lines[0].strip().split(',')
for i in range(tree_max-1):
    start = float(line[i])
    end = float(line[i+1])
    if start>=a and end<=a:
        if start==end:
            b.append(i+1)
        else:
            b.append((start-a)/(start-end)+i+1)
        break

m = 4
for k in range(4):
    l = 0
    line = lines[k+1].strip().split(',')
    for i in range(tree_max-1):
        start = float(line[i])
        end = float(line[i+1])
        if start>=a and end<=a:
            if start==end:
                l = i+1
            else:
                l = (start-a)/(start-end)+i+1

            b.append(b[0]/l*m)
            break
    m = m*4
b[0] = 1


plt.plot(x,b,ms=4,marker = 'o',label='P-MCGS',lw=3)
f_tree.close()



b = []
f_tree = open('final_linearly_speedup_result_naive_tree.txt')
lines = f_tree.readlines()
line = lines[0].strip().split(',')
for i in range(tree_max-1):
    start = float(line[i])
    end = float(line[i+1])
    if start>=a and end<=a:
        if start==end:
            b.append(i+1)
        else:
            b.append((start-a)/(start-end)+i+1)
        break

m = 4
for k in range(4):
    l = 0
    line = lines[k+1].strip().split(',')
    for i in range(tree_max-1):
        start = float(line[i])
        end = float(line[i+1])
        if start>=a and end<=a:
            if start==end:
                l = i+1
            else:
                l = (start-a)/(start-end)+i+1

            b.append(b[0]/l*m)
            break
    m = m*4
b[0] = 1


plt.plot(x,b,ms=4,marker = 'o',label='naive',lw=3)
f_tree.close()


plt.xlabel('number of workers',size = 20)
plt.ylabel('speedup',size = 20)
plt.legend(fontsize = 18)
plt.savefig('MCG_naive_linearly_speedup_tree.pdf')
