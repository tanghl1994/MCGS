from graph_construction import graph
import run_algorithm
import math
import matplotlib.pyplot as plt

mygraph = graph()
print(mygraph)

#machine_number = 300
sample_number = 500
epsilon = 0.1
delta = 0.1
time_list = range(1200)
eta = 0.7
gamma = 1
#algo = 'paper'
a = 0.5*(1+eta)*math.log(4*mygraph.leaf_node_number*(1+eta)/delta/(1-eta))
cm = 1

result1 = []
machine_number = 1
while machine_number <= 256:
    result1.append(run_algorithm.run_algorithm(mygraph, machine_number,sample_number,epsilon, delta, time_list, 0.7, gamma, a, 'paper',cm))
    machine_number = machine_number * 4

result2 = []
machine_number = 1
while machine_number <= 256:
    result2.append(run_algorithm.run_algorithm(mygraph, machine_number,sample_number,epsilon, delta, time_list, 100000, gamma, a, 'naive',cm))
    machine_number = machine_number * 4


my_result = open('final_linearly_speedup_result_MCG_tree.txt','w')
for i in range(5):
    for j in range(len(time_list)-1):
        my_result.write(str(result1[i][j])+',')
    my_result.write(str(result1[i][len(time_list)-1])+'\n')
my_result.close()

my_result = open('final_linearly_speedup_result_naive_tree.txt','w')
for i in range(5):
    for j in range(len(time_list)-1):
        my_result.write(str(result2[i][j])+',')
    my_result.write(str(result2[i][len(time_list)-1])+'\n')
my_result.close()
    
for i in range(5):
    plt.plot(time_list,result1[i],label = str(4**i) + ' machines1',lw = 3)

for i in range(5):
    plt.plot(time_list,result2[i],label = str(4**i) + ' machines2',lw = 3)

plt.xlabel("iterations",size = 21)
plt.ylabel("error",size = 21)
plt.legend(fontsize = 18)
plt.savefig('final_linear_speed_up_tree_MCG_naive.pdf')


