import numpy as np 
import time
import os
import sys

final_node=np.array([[1,2,3],[4,5,6],[7,8,0]])

class node :
    def __init__ (self) :
        self.path=[]
        self.array=np.zeros((3,3),dtype=np.uint8)
        self.h=9-np.count_nonzero(self.array==final_node)
        
def locate_zero(array):
    i=0
    j=0
    while (i<3):
        j=0
        if array[i,j] == 0:
            return [i,j]
        while (j<3):
            if array[i,j] == 0 :
                return [i,j]
            j=j+1
        i=i+1

def possible_moves(array):
    moves_list=[]
    zero_position=locate_zero(array)
    if (zero_position[0]<2) :
        moves_list.append('d')
    if (zero_position[0]>0) :
        moves_list.append('u')
    if (zero_position[1]<2) :
        moves_list.append('r')
    if (zero_position[1]>0) :
        moves_list.append('l')
    return moves_list

def expand(node_x,open_list):
    node_temp=np.copy(node_x.array)
    l=possible_moves(node_temp)
    zero=locate_zero(node_temp)
    for s in l : 
        t=node()
        t.array=np.zeros((3,3),dtype=np.uint8)
        t.path=node_x.path.copy()
        node_temp=np.copy(node_x.array)
        if s=='r':
            try:
                if t.path[-1]=='l':
                    continue
            except: 
                pass            
            temp=node_temp[zero[0],zero[1]+1]
            node_temp[zero[0],zero[1]+1]=0
            node_temp[zero[0],zero[1]]=temp
            t.array=node_temp
            t.path.append('r')
            t.h=(9-np.count_nonzero(t.array==final_node))+len(t.path)
            if (t.h<open_list[0].h)&(len(open_list)!=0):
                open_list.insert(0,t)
            else :
                open_list.append(t)
        if s=='l':
            try:
                if t.path[-1]=='r':
                    continue
            except: 
                pass
            temp=node_temp[zero[0],zero[1]-1]
            node_temp[zero[0],zero[1]-1]=0
            node_temp[zero[0],zero[1]]=temp
            t.array=node_temp
            t.path.append('l')
            t.h=(9-np.count_nonzero(t.array==final_node))+len(t.path)
            if (t.h<open_list[0].h)&(len(open_list)!=0):
                open_list.insert(0,t)
            else :
                open_list.append(t)
        if s=='u':
            try:
                if t.path[-1]=='d':
                    continue
            except: 
                pass
            temp=node_temp[zero[0]-1,zero[1]]
            node_temp[zero[0]-1,zero[1]]=0
            node_temp[zero[0],zero[1]]=temp
            t.array=node_temp
            t.path.append('u')
            t.h=(9-np.count_nonzero(t.array==final_node))+len(t.path)
            if (t.h<open_list[0].h)&(len(open_list)!=0):
                open_list.insert(0,t)
            else :
                open_list.append(t) 
        if s=='d':
            try:
                if t.path[-1]=='u':
                    continue
            except: 
                pass
            temp=node_temp[zero[0]+1,zero[1]]
            node_temp[zero[0]+1,zero[1]]=0
            node_temp[zero[0],zero[1]]=temp
            t.array=node_temp
            t.path.append('d')
            t.h=(9-np.count_nonzero(t.array==final_node))+len(t.path)
            if (t.h<open_list[0].h)&(len(open_list)!=0):
                open_list.insert(0,t)
            else :
                open_list.append(t)  

def node_in_closed_list(node,cl):
    i=0
    while i < len(cl):
        if (node==cl[i]).all()==True :
            return True 
        i=i+1
    return False

def A_H(init_node,time_limit,memory_limit):
    previous_depth=0
    N_nodes_treated=0
    nodes_that_repeats=0
    open_list=[init_node]
    closed_list=[init_node.array]
    if (init_node.array==final_node).all()==True :
        return True
    expand(init_node,open_list)
    init_node.h=9-np.count_nonzero(init_node.array==final_node)
    min_h=init_node.h
    t0= time.clock()
    while N_nodes_treated<100000 :
        if N_nodes_treated > 0 :
            previous_depth=len(first_node.path)
        #### Time limit
        if (time.clock() - t0 > time_limit) :
            print('Over',time_limit,'seconds have passed')
            print('Le nombre des noeuds traités:',N_nodes_treated)
            print('La Longueur de la liste:',len(open_list))
            print('depth reached: ',len(first_node.path))
            print('Memory(open and closed lists) usage: ',(sys.getsizeof(open_list)+sys.getsizeof(closed_list))/1000,' Kbytes')
            print('nodes_that_repeats ',nodes_that_repeats)
            returns=[['No solution in said time'],0,N_nodes_treated,len(open_list),(sys.getsizeof(open_list)+sys.getsizeof(closed_list))/1000,time_limit]
            break
        #### Processing time limit
        if N_nodes_treated==99999 : #stops when procedures takes too much time
            print('Le nombre des noeuds traités a dépasser 10000')
            print('nodes that repeat:',nodes_that_repeats)
            print('depth reached: ',len(first_node.path))
            print('Memory(open and closed lists) usage: ',(sys.getsizeof(open_list)+sys.getsizeof(closed_list))/1000,' Kbytes')
            break
            
        if len(open_list)==0 : 
            return False
        first_node=open_list.pop(0)
        if first_node.h<min_h:
            min_h=first_node.h
            print('dist min h:',min_h,end='\r')
        
        ### Prevent repeating nodes and infinite repeating cycles
        if node_in_closed_list(first_node.array,closed_list): #check if the node is treated before
            nodes_that_repeats=nodes_that_repeats+1
            continue
        
        N_nodes_treated=N_nodes_treated+1 #counts the number of nodes that are gonna be expanded
        closed_list.append(first_node.array) #pour les problèmes de bouclages
        
        #### Memory limit
        if (len(open_list)>memory_limit) :
            print('On a dépasser 10000 noeuds dans la liste, Solution peut être possible mais coûteuse')
            print(nodes_that_repeats)
            print('Memory(open and closed lists) usage: ',(sys.getsizeof(open_list)+sys.getsizeof(closed_list))/1000,' Kbytes')
            print('depth reached: ',len(first_node.path))
            returns=[['No solution under memory limit'],0,N_nodes_treated,len(open_list),(sys.getsizeof(open_list)+sys.getsizeof(closed_list))/1000,time.clock() - t0]
            break
            
        #if len(first_node.path) != previous_depth :
            #print('depth reached: ',len(first_node.path))
        
        if (first_node.array==final_node).all()==True :
            t1 = time.clock() - t0
            N_nodes_treated=N_nodes_treated+1
            print('Solution Possible')
            print('La solution: ',first_node.path)
            print('La longueur de la solution: ',len(first_node.path))
            print('Le nombre des noeuds traités:',N_nodes_treated)
            print('La Longueur de la liste:',len(open_list))
            print('Memory(open and closed lists) usage: ',(sys.getsizeof(open_list)+sys.getsizeof(closed_list))/1000,' Kbytes')
            print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)
            return [first_node.path,len(first_node.path),N_nodes_treated,len(open_list),(sys.getsizeof(open_list)+sys.getsizeof(closed_list))/1000,t1]
        else:
            expand(first_node,open_list)
    return returns
    
