from graph_construction import graph
import run_algorithm
import math
import matplotlib.pyplot as plt
from multiprocessing import Pool
import json

mygraph = graph()
print(mygraph)



sample_number = 1
epsilon = 0.1
delta = 0.1
time_list = range(1000)
eta = 0.7
gamma = 1
#algo = 'paper'
a = 0.5*(1+eta)*math.log(4*mygraph.leaf_node_number*(1+eta)/delta/(1-eta))
cm = 1

result = []
w = []
machine_number = 1
while machine_number <= 256:
    result.append([])
    w.append([])

    result_c = []

    for co in range(5):
        po = Pool(100)
        for p in range(100):
            result_c.append(po.apply_async(run_algorithm.run_algorithm, args=(mygraph, machine_number,sample_number,epsilon,
                                                                       delta, time_list, eta, gamma, a, 'paper',cm)))
        po.close()
        po.join()

    # resulttt,www = run_algorithm.run_algorithm(mygraph, machine_number,sample_number,epsilon, delta, time_list, eta, gamma, a, 'paper',cm)
    for i in range(500):
        result[-1].append(result_c[i].get()[0])
        w[-1].append(result_c[i].get()[1])

    # result.append(resulttt)

    # w.append(www)
    machine_number = machine_number * 4

my_result = open('final_linearly_speedup_result_tree.txt','w')
w_result = open('final_linearly_speedup_result_tree_w.txt','w')
json.dump(result, my_result)
json.dump(w, w_result)
# for i in range(5):
#     for j in range(len(result[0])-1):
#         my_result.write(str(result[i][j])+',')
#         w_result.write(str(w[i][j]) + ',')
#     my_result.write(str(result[i][len(result[0])-1])+'\n')
#     w_result.write(str(w[i][len(result[0]) - 1]) + '\n')
# my_result.close()
    
# for i in range(5):
#     plt.plot(time_list,result[i],label = str(4**i) + ' machines',lw = 3)
#
#
#
#
# #plt.plot(time_list,a1,label = 'graph',lw = 3)
# #plt.plot(time_list,a2,label = 'tree',lw = 3)
#
#
# plt.xlabel("iterations",size = 21)
# plt.ylabel("error",size = 21)
# plt.legend(fontsize = 18)
# plt.savefig('final_linear_speed_up_tree.pdf')
