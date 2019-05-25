import run_uct_new
import math
import run_algorithm
from graph_construction import graph
import matplotlib.pyplot as plt

mygraph = graph()
print(mygraph)
machine_number = 20
epsilon = 0.1
delta = 0.1
sample_number = 500
time_list = range(1000)
eta = 0.7
gamma = 1
a = 0.5*(1+eta)*math.log(4*mygraph.leaf_node_number*(1+eta)/delta/(1-eta))
cm = 1
cp = 1


a1 = run_algorithm.run_algorithm(mygraph, machine_number,sample_number,epsilon, delta, time_list, 0.7, gamma, a, 'paper',cm)
a2 = run_uct_new.run_uct_new(mygraph, machine_number,sample_number,time_list,0.7,gamma,cp)

plt.plot(time_list,a1,label = 'MCG', lw = 3)
plt.plot(time_list,a2,label = 'UCT', lw = 3)

plt.xlabel("iterations",size = 21)
plt.ylabel("error",size = 21)
plt.legend(fontsize = 18)
plt.savefig('test_MCG_UCT_new.pdf')
