from graph_construction import graph
import run_algorithm
import math
import matplotlib.pyplot as plt

mygraph = graph()
print(mygraph)


sample_number = 500
epsilon = 0.1
delta = 0.1
time_list = range(75)
eta = 0.7
gamma = 1
#algo = 'paper'
a = 0.5*(1+eta)*math.log(4*mygraph.leaf_node_number*(1+eta)/delta/(1-eta))
cm = 1

result = []
w =[]
machine_number = 1
while machine_number <= 256:

    resulttt, www = run_algorithm.run_algorithm(mygraph, machine_number,sample_number,epsilon, delta, time_list, eta, gamma, a, 'paper',cm)
    result.append(resulttt)
    w.append(www)

    machine_number = machine_number * 4

my_result = open('final_linearly_speedup_result_graph.txt','w')
w_result = open('final_linearly_speedup_result_graph_w.txt','w')
for i in range(5):
    for j in range(len(time_list)-1):
        my_result.write(str(result[i][j])+',')
        w_result.write(str(w[i][j]) + ',')
    my_result.write(str(result[i][len(time_list)-1])+'\n')
    w_result.write(str(w[i][len(time_list) - 1]) + '\n')
my_result.close()
    
for i in range(5):
    plt.plot(time_list,result[i],label = str(4**i) + ' machines',lw = 3)




#plt.plot(time_list,a1,label = 'graph',lw = 3)
#plt.plot(time_list,a2,label = 'tree',lw = 3)


plt.xlabel("iterations",size = 21)
plt.ylabel("error",size = 21)
plt.legend(fontsize = 18)
plt.savefig('final_linear_speed_up_graph.pdf')
