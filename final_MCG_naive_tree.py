from graph_construction import graph
import run_algorithm
import math
import matplotlib.pyplot as plt

mygraph = graph()
print(mygraph)

machine_number = 300
sample_number = 500
epsilon = 0.1
delta = 0.1
time_list = range(1200)
eta = 0.7
gamma = 1
#algo = 'paper'
a = 0.5*(1+eta)*math.log(4*mygraph.leaf_node_number*(1+eta)/delta/(1-eta))
cm = 1



a1 = run_algorithm.run_algorithm(mygraph, machine_number,sample_number,epsilon, delta, time_list, 0.7, gamma, a, 'paper',cm)
a2 = run_algorithm.run_algorithm(mygraph, machine_number,sample_number,epsilon, delta, time_list, 100000, gamma, a, 'naive',cm)


plt.plot(time_list,a1,label = 'P-MCG',lw = 3)
plt.plot(time_list,a2,label = 'naive',lw = 3)


plt.xlabel("iterations",size = 21)
plt.ylabel("error",size = 21)
plt.legend(fontsize = 18)
plt.savefig('final_MCG_naive_tree_new_test.pdf')
