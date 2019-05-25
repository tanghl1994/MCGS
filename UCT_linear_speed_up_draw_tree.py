import matplotlib.pyplot as plt
plt.figure(figsize = (12,6))
plt.subplot(1,2,1)
file_name_tree = 'UCT_final_linearly_speedup_result_tree.txt'
f_tree = open(file_name_tree)
tree_max = 60
lines = f_tree.readlines()
m = 1
for k in range(5):
    a = []
    b = []
    line = lines[k]
    line = line.strip().split(',')
    for i in range(tree_max):
        a.append((i+1)/tree_max/m)
        b.append(float(line[i]))
        if b[-1] == 0:
            break
    plt.plot(a,b,label = str(m)+' machines',lw=3)

    m = m * 4

plt.xlabel('normalized time',size = 25)
plt.ylabel('error',size = 25)
plt.legend(loc='upper right',fontsize = 13)
#plt.savefig('speedup2.pdf')
plt.subplot(1,2,2)

f_tree.close()



x = [1,4,16,64,256]
plt.plot(x,x,ms = 4,marker = 'o',label='ideal',lw=3)
alist = [0.04,0.02,0.01]
for a in alist:
    b = []
    f_tree = open('UCT_final_linearly_speedup_result_tree.txt')
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


    plt.plot(x,b,ms=4,marker = 'o',label='error='+str(a),lw=3)
    f_tree.close()

##a = 0.01
##b = []
##f = open('result'+str(1)+'.txt')
##lines = f.readlines()
##for i in range(39):
##    start = float(lines[i].strip())
##    end = float(lines[i+1].strip())
##    if start>=a and end<=a:
##        if start==end:
##            b.append(1000*(i+1))
##        else:
##            b.append(1000*((start-a)/(start-end)+i+1))
##        break
##
##m = 2
##for k in range(7):
##    l = 0
##    f = open('result'+str(m)+'.txt')
##    lines = f.readlines()
##    for i in range(39):
##        start = float(lines[i].strip())
##        end = float(lines[i+1].strip())
##        if start>=a and end<=a:
##            if start==end:
##                l = (1000*(i+1))
##            else:
##                l = (1000*((start-a)/(start-end)+i+1))
##
##            b.append(b[0]/l*m)
##            break
##    m = m*2
##b[0] = 1
##plt.plot(x,b,ms = 4,marker = 'o',label = 'error=0.01',lw=3)
##
##a = 0.001
##b = []
##f = open('result'+str(1)+'.txt')
##lines = f.readlines()
##for i in range(39):
##    start = float(lines[i].strip())
##    end = float(lines[i+1].strip())
##    if start>=a and end<=a:
##        if start==end:
##            b.append(1000*(i+1))
##        else:
##            b.append(1000*((start-a)/(start-end)+i+1))
##        break
##
##m = 2
##for k in range(7):
##    l = 0
##    f = open('result'+str(m)+'.txt')
##    lines = f.readlines()
##    for i in range(39):
##        start = float(lines[i].strip())
##        end = float(lines[i+1].strip())
##        if start>=a and end<=a:
##            if start==end:
##                l = (1000*(i+1))
##            else:
##                l = (1000*((start-a)/(start-end)+i+1))
##
##            b.append(b[0]/l*m)
##            break
##    m = m*2
##b[0] = 1
##plt.plot(x,b,ms=4,marker = 'o',label = 'error=0.001',lw=3)
plt.xlabel('number of workers',size = 25)
plt.ylabel('speedup',size = 25)
plt.legend(fontsize = 18)
plt.savefig('UCT_linearly_speedup_tree.pdf')
