import random
import graph_construction
import math
import bisect


graph_meta_information = []     #sample mean, Lower bound, Upper bound observed times, unobserved times
machine_meta_information = []   #which node, next time available
node_available_time = []


def produce_01(mean):
    if random.random() < mean:
        return 1
    else:
        return 0

def compute_halfinterval_test(node,delta,t):
    return 0.1

def compute_halfinterval_origin(node,delta,t,eta,gamma,leaf):
    n = graph_meta_information[node]['observed_times']
    b = math.log(leaf/delta) + 3*math.log(math.log(leaf/delta)) + 3/2*math.log(math.log(n)+1)
    return math.sqrt(b/2/n)

def compute_halfinterval_always_observed_time(node,delta,t,leaf):
    n = graph_meta_information[node]['observed_times']
    b = math.log(math.pi)+1/2*math.log(leaf/3/delta)+math.log(n)
    return math.sqrt(b/n)

def compute_halfinterval_total_time(node,delta,t,leaf):
    n = graph_meta_information[node]['observed_times'] + tree_meta_information[node]['unobserved_times']
    b = math.log(math.pi)+1/2*math.log(leaf/3/delta)+math.log(n)
    return math.sqrt(b/n)

def compute_halfinterval_paper(node,delta,t,eta,gamma,leaf,a,cm):
    o = graph_meta_information[node]['observed_times']
    u = graph_meta_information[node]['unobserved_times']
#    a = 0.5*(1+eta*gamma)*math.log(4*leaf*(1+gamma*eta)/delta/(1-gamma*eta))
#    print(a)
    b = a + math.log(o + gamma*u)
    return cm*math.sqrt(b/(o+gamma*u))

def compute_halfinterval_naive(node,delta,t,eta,gamma,leaf,a,cm):
    o = graph_meta_information[node]['observed_times']
    u = graph_meta_information[node]['unobserved_times']
#    a = 0.5*(1+eta*gamma)*math.log(4*leaf*(1+gamma*eta)/delta/(1-gamma*eta))
    b = a + math.log(o)
    return cm*math.sqrt(b/(o))


    
    


def initialize(mygraph, machine_number, compute_halfinterval,delta,eta,gamma,a,cm):
    #initialize graph meta information
    t = 0
    for node in range(mygraph.node_number):
        graph_meta_information.append({})
    for node in range(mygraph.node_number-1,-1,-1):
        if mygraph.structure[node] == []:
            graph_meta_information[node]['sample_mean'] = produce_01(mygraph.node_value[node])
            graph_meta_information[node]['observed_times'] = 1
            graph_meta_information[node]['unobserved_times'] = 0
            half_interval = compute_halfinterval(node,delta,t,eta,gamma,mygraph.leaf_node_number,a,cm)
            graph_meta_information[node]['lower_bound'] = max(graph_meta_information[node]['sample_mean'] - half_interval, 0)
            graph_meta_information[node]['upper_bound'] = min(graph_meta_information[node]['sample_mean'] + half_interval, 1)
            t = t + 1
        else:
            if mygraph.node_type[node] == 'max':
                graph_meta_information[node]['lower_bound'] = max([graph_meta_information[childnode]['lower_bound'] \
                                                                   for childnode in mygraph.structure[node]])
                graph_meta_information[node]['upper_bound'] = max([graph_meta_information[childnode]['upper_bound'] \
                                                                   for childnode in mygraph.structure[node]])
            else:
                graph_meta_information[node]['lower_bound'] = min([graph_meta_information[childnode]['lower_bound'] \
                                                                   for childnode in mygraph.structure[node]])
                graph_meta_information[node]['upper_bound'] = min([graph_meta_information[childnode]['upper_bound'] \
                                                                   for childnode in mygraph.structure[node]])

    #initialize machine meta information
    for machine in range(machine_number):
        machine_meta_information.append({})
        machine_meta_information[machine]['node'] = -1
        machine_meta_information[machine]['time_available'] = 0

    #initialize node available time
    for node in range(mygraph.node_number):
        node_available_time.append([])

    return t


def print_information(mygraph,machine_number):

    print('Graph meta information: ')
    for node in range(mygraph.node_number):
        print('node %d: ' % (node), end='')
        print(graph_meta_information[node])
    print()
    print('Machine meta information: ')
    for machine in range(machine_number):
        print('machine %d: ' % (machine), end='')
        print(machine_meta_information[machine])
    print()
    print()

    return



def observe(mygraph, machine, compute_halfinterval,epsilon,delta,t,T,eta,gamma, machine_number,ca,cm):
    #choose the next node to observe
    first_layer_upper = [graph_meta_information[node]['upper_bound'] \
                         for node in mygraph.structure[0]]
    first_layer_lower = [graph_meta_information[node]['lower_bound'] \
                         for node in mygraph.structure[0]]
    B = []

    rv = -1
    for node in mygraph.structure[0]:
        upper = first_layer_upper[:]
        upper.pop(node-1)
        B.append(max(upper) - first_layer_lower[node-1])
    a = B.index(min(B))
    upper2 = first_layer_upper[:]
    upper2.pop(a)
    b = first_layer_upper.index(max(upper2))
    if a==b:
        b = upper2.index(max(upper2))+1

    #stop rule
    if t == T:
        rv = a+1

    #choose represent node
    if first_layer_upper[a] - first_layer_lower[a] >= first_layer_upper[b] - first_layer_lower[b]:
        choosenext = a + 1
    else:
        choosenext = b + 1

    while mygraph.node_type[choosenext]!='leaf':
        if mygraph.node_type[choosenext] == 'max':
            next_layer_upper = [graph_meta_information[node]['upper_bound'] \
                                for node in mygraph.structure[choosenext]]
            choosenext = mygraph.structure[choosenext][next_layer_upper.index(max(next_layer_upper))]
        else:
            next_layer_lower = [graph_meta_information[node]['lower_bound'] \
                                for node in mygraph.structure[choosenext]]
            choosenext = mygraph.structure[choosenext][next_layer_lower.index(min(next_layer_lower))]


    if graph_meta_information[choosenext]['unobserved_times'] > eta*graph_meta_information[choosenext]['observed_times']:
        machine_meta_information[machine]['node'] = -1
        machine_meta_information[machine]['time_available'] = node_available_time[choosenext][0] + 0.000001
        return -2
    
    #update machine information
    machine_meta_information[machine]['node'] = choosenext
    if mygraph.node_time[choosenext] != 'unleaf':
        if mygraph.node_time[choosenext] == 'random':
            machine_meta_information[machine]['time_available'] += random.random()
        else:
            machine_meta_information[machine]['time_available'] += mygraph.node_time[choosenext]
        if eta*graph_meta_information[choosenext]['observed_times'] <= machine_number:
            bisect.insort(node_available_time[choosenext],machine_meta_information[machine]['time_available'])

    #update node information
    graph_meta_information[choosenext]['unobserved_times'] += 1
    half_interval = compute_halfinterval(choosenext,delta,t,eta,gamma,mygraph.leaf_node_number,ca,cm)
    graph_meta_information[choosenext]['lower_bound'] = max(\
        graph_meta_information[choosenext]['sample_mean'] - half_interval, graph_meta_information[choosenext]['lower_bound'])
    graph_meta_information[choosenext]['upper_bound'] = min(\
        graph_meta_information[choosenext]['sample_mean'] + half_interval, graph_meta_information[choosenext]['upper_bound'])

    #update parent information
    for node in range(mygraph.node_number-1,-1,-1):
        if mygraph.structure[node] != []:
            if mygraph.node_type[node] == 'max':
                graph_meta_information[node]['lower_bound'] = max([graph_meta_information[childnode]['lower_bound'] \
                                                                   for childnode in mygraph.structure[node]])
                graph_meta_information[node]['upper_bound'] = max([graph_meta_information[childnode]['upper_bound'] \
                                                                   for childnode in mygraph.structure[node]])
            else:
                graph_meta_information[node]['lower_bound'] = min([graph_meta_information[childnode]['lower_bound'] \
                                                                   for childnode in mygraph.structure[node]])
                graph_meta_information[node]['upper_bound'] = min([graph_meta_information[childnode]['upper_bound'] \
                                                                   for childnode in mygraph.structure[node]])
        
    return rv


def update_result(mygraph, machine, compute_halfinterval,delta,t,eta,gamma,a,cm):
    #update node information
    node = machine_meta_information[machine]['node']
    if node_available_time[node] != []:
        node_available_time[node].pop(0)
    result = produce_01(mygraph.node_value[node])
    graph_meta_information[node]['sample_mean'] = (graph_meta_information[\
        node]['sample_mean']*graph_meta_information[node]['observed_times'] + result)/(\
            graph_meta_information[node]['observed_times']+1)
    graph_meta_information[node]['observed_times'] += 1
    graph_meta_information[node]['unobserved_times'] -= 1
    half_interval = compute_halfinterval(node,delta,t,eta,gamma,mygraph.leaf_node_number,a,cm)
    graph_meta_information[node]['lower_bound'] = max(\
        graph_meta_information[node]['sample_mean'] - half_interval, graph_meta_information[node]['lower_bound'])
    graph_meta_information[node]['upper_bound'] = min(\
        graph_meta_information[node]['sample_mean'] + half_interval, graph_meta_information[node]['upper_bound'])

    #update parent information
    for node in range(mygraph.node_number-1,-1,-1):
        if mygraph.structure[node] != []:
            if mygraph.node_type[node] == 'max':
                graph_meta_information[node]['lower_bound'] = max([graph_meta_information[childnode]['lower_bound'] \
                                                                   for childnode in mygraph.structure[node]])
                graph_meta_information[node]['upper_bound'] = max([graph_meta_information[childnode]['upper_bound'] \
                                                                   for childnode in mygraph.structure[node]])
            else:
                graph_meta_information[node]['lower_bound'] = min([graph_meta_information[childnode]['lower_bound'] \
                                                                   for childnode in mygraph.structure[node]])
                graph_meta_information[node]['upper_bound'] = min([graph_meta_information[childnode]['upper_bound'] \
                                                                   for childnode in mygraph.structure[node]])
    

def parallel_BAI(mygraph, machine_number, algorithm, ifoutput, epsilon,delta,time_list,eta,gamma,a,resulttt,cm,w):
    compute_halfinterval = eval('compute_halfinterval_'+algorithm)
    t = initialize(mygraph, machine_number, compute_halfinterval,delta,eta,gamma,a,cm)
    tt = t
    i = 0 #indicate time_list
    
    if ifoutput == True:
        print('Result of Initialization: ')
        print_information(mygraph,machine_number)
        print()
        
    machine = 0
    output = -1

    while True:
        m = observe(mygraph, machine,compute_halfinterval,epsilon,delta,t,time_list[i]+tt,eta,gamma, machine_number,a,cm)
        if m > 0:
            output = m
            resulttt[i] += mygraph.node_value[0] - mygraph.node_value[output]
            w.append(machine)
            i = i + 1
            if i == len(time_list):
                break
            t = t+1
        if m==-1:
            t = t+1
        if m==-1 and ifoutput==True:
            print('Observe node %d using machine %d' % (machine_meta_information[machine]['node'], machine))
            print()
            print_information(mygraph,machine_number)
            print()
        
        tvalue = [machine_meta_information[m]['time_available'] for m in range(machine_number)]
        machine = tvalue.index(min(tvalue))        

        if machine_meta_information[machine]['node'] != -1:
            update_result(mygraph, machine, compute_halfinterval,delta,t,eta,gamma,a,cm)
            if ifoutput==True:
                print('Node %d in machine %d has finished observing' %
                      (machine_meta_information[machine]['node'], machine))
                print()
                print_information(mygraph,machine_number)
                print()

    if ifoutput==True:
        print('The output node is %d;  Observe %d times'  % (output,t))

#    return output, t


def run_algorithm(mygraph, machine_number, sample_number, epsilon, delta, time_list, eta, gamma, a, algo,cm):
    global graph_meta_information, machine_meta_information, node_available_time
    accuracy = 0
    stop_time = 0
    resulttt = []
    w = []
    for T in time_list:
        resulttt.append(0)
#    for T in time_list:
    for j in range(sample_number):
        print(j)
        graph_meta_information = []     #sample mean, Lower bound, Upper bound observed times, unobserved times
        machine_meta_information = []   #which node, next time available
        node_available_time = []
        parallel_BAI(mygraph, machine_number, algo, False,epsilon,delta,time_list,eta,gamma,a,resulttt,cm,w)
#            accuracy += mygraph.node_value[0] - mygraph.node_value[output]
#        accuracy = accuracy/sample_number
    resulttt = [r/sample_number for r in resulttt]
#    resulttt.append(accuracy)


    return resulttt, w
    



    


