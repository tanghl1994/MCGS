class graph:
    def __init__(self):
        self.node_number = 1     #root node
        self.structure = []
        self.node_type = []
        self.node_value = []     #suppose the value is in [0,1]
        self.node_time = []
        self.node_parent = []

        #construct the tree
        print('Construct the Graph:')
        self.node_parent.append([-1])

        print('Input the number of nodes: ')
        self.node_number = int(input())

        for node in range(self.node_number-1):
            self.node_parent.append([])
            self.structure.append([])
        self.structure.append([])
        

        for node in range(self.node_number):
            print('Please input the child nodes of node %d' % (node))
            child = input()
            if child != '':
                child = child.split(',')
                child = [int(node1) for node1 in child]

                for children in child:
                    self.structure[node].append(children)
                    self.node_parent[children].append(node)



        #construct the type
        self.node_type.append('max')
        for node in range(1,self.node_number):
            if self.structure[node] == []:
                self.node_type.append('leaf')
            else:
                print('Please input the type of node %d' % (node))
                self.node_type.append(input())


        #construct the value
        for node in range(self.node_number):
            self.node_value.append(0)

        for node in range(self.node_number-1,-1,-1):
            if self.structure[node]!=[]:
                if self.node_type[node]=='max':
                    self.node_value[node] = max([self.node_value[child_node] for child_node in \
                                                  self.structure[node]])
                else:
                    self.node_value[node] = min([self.node_value[child_node] for child_node in \
                                                  self.structure[node]])
            else:
                print('Please input the value of node %d' % (node))
                self.node_value[node] = float(input())


        #construct the time
        for node in range(self.node_number):
            self.node_time.append(0)

        for node in range(self.node_number):
            if self.structure[node] == []:
                print('Please input the sample time of node %d' % (node))
                sample_time = input()
                if sample_time!='random':
                    sample_time = float(sample_time)
                    self.node_time[node] = sample_time
                else:
                    self.node_time[node] = 'random'
            else:
                self.node_time[node] = 'unleaf'



        self.leaf_node_number = 0
        for node in range(self.node_number):
            if self.structure[node] == []:
                self.leaf_node_number += 1
        



        



    def __str__(self):
        print('Information of the tree:')
        print()
        print('Number of nodes: %d' % (self.node_number))
        print()
        print('Children of nodes:')
        print(self.structure)
        print()
        print('Parent of nodes:')
        print(self.node_parent)
        print()
        print('Type of nodes:')
        print(self.node_type)
        print()
        print('value of nodes:')
        print(self.node_value)
        print()
        print('Test time of nodes:')
        print(self.node_time)
        print()
        print('Number of leaf nodes:')
        print(self.leaf_node_number)
        print()
        
        return ''


if __name__ == '__main__':
    test_graph = graph()
    print(test_graph)
                   
        
        

                    
            
                





            

       
