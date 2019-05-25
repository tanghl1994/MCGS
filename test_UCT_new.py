import run_uct_new
import math
from graph_construction import graph
import matplotlib.pyplot as plt

mygraph = graph()
print(mygraph)
machine_number = 20
sample_number = 20
time_list = range(10000)
eta = 0.7
gamma = 1
cp = 1



a2 = run_uct_new.run_uct_new(mygraph, machine_number,sample_number,time_list,eta,gamma,cp)

#plt.plot(time_list,a1,label = 'MCG', lw = 3)
plt.plot(time_list,a2,label = 'UCT', lw = 3)

plt.xlabel("iterations",size = 21)
plt.ylabel("error",size = 21)
plt.legend(fontsize = 18)
plt.savefig('test_UCT_new.pdf')
