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



def compute_halfinterval(node,gamma,leaf,cp,to,tu):
    o = graph_meta_information[node]['observed_times']
    u = graph_meta_information[node]['unobserved_times']
#    a = 0.5*(1+eta*gamma)*math.log(4*leaf*(1+gamma*eta)/delta/(1-gamma*eta))
#    print(a)
#    b = a + math.log(o + gamma*u)
#    return cm*math.sqrt(b/(o+gamma*u))
    return cp*math.sqrt(math.log(to+gamma*tu)/(o+gamma*u))




    
    


def initialize(mygraph, machine_number, compute_halfinterval,eta,gamma,cp):
    #initialize graph meta information
    t = 0
    for node in range(mygraph.node_number):
        graph_meta_information.append({'sample_mean':0, 'observed_times':0, 'unobserved_times':0})
    for node in range(mygraph.node_number-1,-1,-1):
        if mygraph.structure[node] == []:
            result = produce_01(mygraph.node_value[node])
            this_set = [node]
            flag_set = [0 for i in range(mygraph.node_number)]
            while this_set != []:
                #print(this_set)
                this_node = this_set[0]
                if flag_set[this_node] == 0:
                    flag_set[this_node] = 1
                    graph_meta_information[this_node]['sample_mean'] = (graph_meta_information[
                        this_node]['sample_mean']*graph_meta_information[this_node]['observed_times'] + result)/(\
                            graph_meta_information[this_node]['observed_times']+1)
                    graph_meta_information[this_node]['observed_times'] += 1
                    if mygraph.node_parent[this_node]!=[-1]:
                        this_set = this_set + mygraph.node_parent[this_node]
                    #print("how? %d, %d" % (this_node, graph_meta_information[56]['observed_times']))
                this_set.pop(0)
            t = t + 1
                        
##    for node in range(mygraph.node_number-1,-1,-1):
##        if mygraph.structure[node] == []:
##            graph_meta_information[node]['sample_mean'] = produce_01(mygraph.node_value[node])
##            graph_meta_information[node]['observed_times'] = 1
##            graph_meta_information[node]['unobserved_times'] = 0
###            half_interval = compute_halfinterval(node,gamma,mygraph.leaf_node_number,cp,t,0)
###            graph_meta_information[node]['lower_bound'] = graph_meta_information[node]['sample_mean'] - half_interval
###            graph_meta_information[node]['upper_bound'] = graph_meta_information[node]['sample_mean'] + half_interval
##            t = t + 1
                
    for node in range(mygraph.node_number):
#        if mygraph.structure[node]!=[]:
#            child_mean = [graph_meta_information[child]['sample_mean'] for child in mygraph.structure[node]]
#            graph_meta_information[node]['observed_times'] = len(child_mean)
#            graph_meta_information[node]['sample_mean'] = sum(child_mean)/len(child_mean)
#            graph_meta_information[node]['unobserved_times'] = 0
        half_interval = compute_halfinterval(node,gamma,mygraph.leaf_node_number,cp,t,0)
        graph_meta_information[node]['lower_bound'] = graph_meta_information[node]['sample_mean'] - half_interval
        graph_meta_information[node]['upper_bound'] = graph_meta_information[node]['sample_mean'] + half_interval

            
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



def observe(mygraph, machine, compute_halfinterval,t,T,eta,gamma, machine_number,cp):

    #choose the next node to observe
    rv = -1
    if t==T:
        m = [graph_meta_information[node]['sample_mean'] for node in mygraph.structure[0]]
        rv = m.index(max(m)) + 1
    choosenext = 0
    

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
    this_set = [choosenext]
    flag_set = [0 for i in range(mygraph.node_number)]
    while this_set != []:
        this_node = this_set[0]
        if flag_set[this_node] == 0:
            flag_set[this_node] = 1
            graph_meta_information[this_node]['unobserved_times'] += 1
            if mygraph.node_parent[this_node]!=[-1]:
                this_set = this_set + mygraph.node_parent[this_node]
        this_set.pop(0)


            
##    graph_meta_information[choosenext]['unobserved_times'] += 1
##    parent = mygraph.node_parent[choosenext][0]
##    while parent > 0:
##        graph_meta_information[parent]['unobserved_times'] += 1
##        parent = mygraph.node_parent[parent][0]
    
    to = graph_meta_information[0]['observed_times']
    tu = graph_meta_information[0]['unobserved_times']

    for node in range(mygraph.node_number):
        half_interval = compute_halfinterval(node,gamma,mygraph.leaf_node_number,cp,to,tu)
        graph_meta_information[node]['lower_bound'] = graph_meta_information[node]['sample_mean'] - half_interval
        graph_meta_information[node]['upper_bound'] = graph_meta_information[node]['sample_mean'] + half_interval


        
    return rv


def update_result(mygraph, machine, compute_halfinterval,t,eta,gamma,cp):
    #update node information
    node = machine_meta_information[machine]['node']
    if node_available_time[node] != []:
        node_available_time[node].pop(0)

    result = produce_01(mygraph.node_value[node])

    this_set = [node]
    flag_set = [0 for i in range(mygraph.node_number)]
    while this_set != []:
        this_node = this_set[0]
        if flag_set[this_node] == 0:
            flag_set[this_node] = 1
            graph_meta_information[this_node]['sample_mean'] = (graph_meta_information[\
                this_node]['sample_mean']*graph_meta_information[this_node]['observed_times'] + result)/(\
                    graph_meta_information[this_node]['observed_times']+1)
            graph_meta_information[this_node]['observed_times'] += 1
            graph_meta_information[this_node]['unobserved_times'] -= 1
            if mygraph.node_parent[this_node]!=[-1]:
                this_set = this_set + mygraph.node_parent[this_node]
        this_set.pop(0)



##    
##    graph_meta_information[node]['sample_mean'] = (graph_meta_information[\
##        node]['sample_mean']*graph_meta_information[node]['observed_times'] + result)/(\
##            graph_meta_information[node]['observed_times']+1)
##    graph_meta_information[node]['observed_times'] += 1
##    graph_meta_information[node]['unobserved_times'] -= 1
##
##    parent = mygraph.node_parent[node][0]
##    while parent>0:
##        graph_meta_information[parent]['sample_mean'] = (graph_meta_information[\
##            parent]['sample_mean']*graph_meta_information[parent]['observed_times'] + result)/(\
##                graph_meta_information[parent]['observed_times']+1)
##        graph_meta_information[parent]['observed_times'] += 1
##        graph_meta_information[parent]['unobserved_times'] -= 1
##        parent = mygraph.node_parent[parent][0]

    to = graph_meta_information[0]['observed_times']
    tu = graph_meta_information[0]['unobserved_times']

    for node in range(mygraph.node_number):
        half_interval = compute_halfinterval(node,gamma,mygraph.leaf_node_number,cp,to,tu)
        graph_meta_information[node]['lower_bound'] = graph_meta_information[node]['sample_mean'] - half_interval
        graph_meta_information[node]['upper_bound'] = graph_meta_information[node]['sample_mean'] + half_interval
    

    

def parallel_BAI(mygraph, machine_number, ifoutput, time_list,cp,eta,gamma,resulttt):
#    compute_halfinterval = eval('compute_halfinterval_'+algorithm)
    compute_halfinterval = eval('compute_halfinterval')
    t = initialize(mygraph, machine_number, compute_halfinterval,eta,gamma,cp)
    tt = t
    i = 0 #indicate time_list
    
    if ifoutput == True:
        print('Result of Initialization: ')
        print_information(mygraph,machine_number)
        print()
        
    machine = 0
    output = -1

    while True:
        m = observe(mygraph, machine,compute_halfinterval,t,time_list[i]+tt,eta,gamma, machine_number,cp)
#        print_information(mygraph,machine_number)
        if m > 0:
            output = m
            resulttt[i] += mygraph.node_value[0] - mygraph.node_value[output]
            i = i + 1
            if i == len(time_list):
                break
            t = t+1
        if m==-1:
            t = t+1
        if ifoutput==True:
            print('Observe node %d using machine %d' % (machine_meta_information[machine]['node'], machine))
            print()
            print_information(mygraph,machine_number)
            print()
        
        tvalue = [machine_meta_information[m]['time_available'] for m in range(machine_number)]
        machine = tvalue.index(min(tvalue))        

#        print(1)
        if machine_meta_information[machine]['node'] != -1:
            update_result(mygraph, machine, compute_halfinterval,t,eta,gamma,cp)
            if ifoutput==True:
                print('Node %d in machine %d has finished observing' %
                      (machine_meta_information[machine]['node'], machine))
                print()
                print_information(mygraph,machine_number)
                print()
#        print(2)

    if ifoutput==True:
        print('The output node is %d;  Observe %d times'  % (output,t))

#    return output, t


def run_uct_new(mygraph, machine_number, sample_number, time_list, eta, gamma, cp):
    global graph_meta_information, machine_meta_information, node_available_time
    accuracy = 0
    stop_time = 0
    resulttt = []
    for T in time_list:
        resulttt.append(0)
#    for T in time_list:
    for j in range(sample_number):
        print(j)
        graph_meta_information = []     #sample mean, Lower bound, Upper bound observed times, unobserved times
        machine_meta_information = []   #which node, next time available
        node_available_time = []
        parallel_BAI(mygraph, machine_number, False,time_list,cp,eta,gamma,resulttt)
#            accuracy += mygraph.node_value[0] - mygraph.node_value[output]
#        accuracy = accuracy/sample_number
    resulttt = [r/sample_number for r in resulttt]
#    resulttt.append(accuracy)


    return resulttt
    



    


