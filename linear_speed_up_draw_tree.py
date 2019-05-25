import matplotlib.pyplot as plt
import json

plt.figure(figsize = (12,6))
plt.subplot(1,2,1)
file_name_tree = 'final_linearly_speedup_result_tree.txt'
w_tree = 'final_linearly_speedup_result_tree_w.txt'
wp = open(w_tree, 'r')
fp = open(file_name_tree, 'r')
# wp = open(w_tree, 'r')
w = json.load(wp)
result = json.load(fp)
# w = json.load(wp)
# f_tree = open(file_name_tree)
tree_max = 5000
# lines = f_tree.readlines()
# m = 1
# for k in range(5):
#     a = []
#     b = []
#     line = lines[k]
#     line = line.strip().split(',')
#     for i in range(tree_max):
#         a.append((i+1)/tree_max/m)
#         b.append(float(line[i]))
#         if b[-1] == 0:
#             break
#     plt.plot(a,b,label = str(m)+' machines',lw=3)
#
#     m = m * 4
aaa = [sum([result[0][j][i] for j in range(500)])/500 for i in range(tree_max)]
plt.plot(range(tree_max),aaa)
# plt.xlabel('normalized time',size = 25)
# plt.ylabel('error',size = 25)
# plt.legend(loc='upper right',fontsize = 13)
# #plt.savefig('speedup2.pdf')
plt.subplot(1,2,2)
#
# f_tree.close()



x = [1,4,16,64,256]
plt.plot(x,x,ms = 4,marker = 'o',label='ideal',lw=3)
alist = [0.1,0.05,0.01,0.005]

for a in alist:
    b = []
    # f_tree = open('final_linearly_speedup_result_tree.txt')
    # w_tree = open('final_linearly_speedup_result_graph_w.txt')
    # lines = f_tree.readlines()
    # line = lines[0].strip().split(',')
    # ws = w_tree.readlines()
    bb = []
    for r in range(500):
        for i in range(tree_max-1):
            start = float(result[0][r][i])
            end = float(result[0][r][i+1])
            if start>=a and end<=a:
                if start==end:
                    bb.append(i+1)
                else:
                    bb.append((start-a)/(start-end)+i+1)
                break
    b.append(sum(bb)/500)

    m = 4
    for k in range(4):
        l = 0
        # line = lines[k+1].strip().split(',')
        # w = ws[k + 1].strip().split(',')
        # w = [int(x) for x in w]
        bb = []
        for r in range(500):
            for i in range(tree_max-1):
                start = float(result[k+1][r][i])
                end = float(result[k+1][r][i+1])
                if start>=a and end<=a:
                    if start==end:
                        l = i+1
                    else:
                        l = (start-a)/(start-end)+i+1

                    bb.append(max([sum([1 for i in range(int(l)) if w[k+1][r][i] == o]) for o in range(m)]))


                    break
        b.append(b[0] / (sum(bb)/500))
        m = m*4
    b[0] = 1


    plt.plot(x,b,ms=4,marker = 'o',label='error='+str(a),lw=3)
    # f_tree.close()

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
plt.savefig('linearly_speedup_tree.pdf')
