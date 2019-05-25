from graph_construction import graph
import run_algorithm
import math
import matplotlib.pyplot as plt
import run_uct

mygraph = graph()
mytree = graph()
print(mygraph)
print(mytree)

machine_number = 100
sample_number = 500
epsilon = 0.1
delta = 0.1
time_list = range(67,2000,1)
eta = 0.7
gamma = 1
#algo = 'paper'
a = 0.5*(1+eta)*math.log(4*mygraph.leaf_node_number*(1+eta)/delta/(1-eta))
cm = 1
cp = 1



a1 = run_algorithm.run_algorithm(mygraph, machine_number,sample_number,epsilon, delta, time_list, eta, gamma, a, 'paper',cm)
a2 = run_algorithm.run_algorithm(mytree, machine_number,sample_number,epsilon, delta, time_list, eta, gamma, a, 'paper',cm)
a3 = run_uct.run_uct_new(mytree,machine_number,sample_number, time_list, eta, gamma,cp)


plt.plot(time_list,a1,label = 'acyclic graph',lw = 3)
plt.plot(time_list,a2,label = 'expanded tree(P-MCGS)',lw = 3)
plt.plot(time_list,a3,label = 'expanded tree(P-UCT)', lw = 3)


plt.xlabel("iterations",size = 21)
plt.ylabel("error",size = 21)
plt.legend(loc = 'upper right', fontsize = 15)
plt.savefig('final_MCG_MCT_UCT.pdf')
