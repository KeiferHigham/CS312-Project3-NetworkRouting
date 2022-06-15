#!/usr/bin/python3


from CS312Graph import *
import time
import math


class NetworkRoutingSolver:
    def __init__( self):
        self.network = None
        self.result = []

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE


        path_edges = []
        total_length = 0
        for i in self.result:
            if i.id == self.network.nodes[destIndex].node_id:
                dest = self.network.nodes[destIndex]
                while(dest.node_id != self.network.nodes[self.source].node_id):
                    source = self.find_prev(dest,self.result)
                    Length = 0
                    for k in source.neighbors:
                        if k.dest == dest:
                            Length = k.length
                    path_edges.append((source.loc,dest.loc,'{:.0f}'.format(Length)))
                    total_length += Length
                    dest = source
                return {'cost': total_length, 'path': path_edges}






    def find_prev(self,node,shortest_path):
        list = []
        for i in shortest_path:
            if i.id == node.node_id:
                list.append(i.prev)
       # for i in range(len(self.network.nodes)):
           # if self.network.nodes[i].node_id == list[0].id:
                #return self.network.nodes[i]
        return self.network.nodes[list[0].id]










       # path_edges = []
       # total_length = 0
       # node = self.network.nodes[self.source]
       # edges_left = 3
       # while edges_left > 0:
       #     edge = node.neighbors[2]
        #    path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
        #    total_length += edge.length
        #    node = edge.dest
        #    edges_left -= 1
       # return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)

        if(use_heap == False):
            Q = ArrayPriorityQueue()
        else:
            Q = BinaryHeapPriorityQueue()

        self.result = []
        for i in self.network.nodes:
            if i.node_id  == srcIndex:
                Q.insert(Node(i.node_id ,0 ,i.node_id,i.neighbors))
                self.result.append(Node(i.node_id,0,i.node_id,i.neighbors))
            else:
                Q.insert(Node(None,math.inf,i.node_id,i.neighbors))
                self.result.append(Node(None, math.inf,i.node_id,i.neighbors))
        Q.current_size = len(self.network.nodes)
        while len(Q.nodes) != 0:
            u = Q.delete_min()
            neighbors = u.neighbors
            x = u.distance
            for i in neighbors:
                alt = x + i.length
                indexToDecrease = i.dest.node_id
                if alt < self.result[indexToDecrease].distance:
                    self.result[indexToDecrease].prev = u
                    self.result[indexToDecrease].distance = alt
                    Q.decrease_key(self.result[indexToDecrease].id, alt)

        t2 = time.time()
        return (t2-t1)







class ArrayPriorityQueue:
    nodes = []
    pointers = {}
    current_size = 0

    # This will be a constant time O(1) operation just insert the node
    def insert(self,node):
        self.nodes.append(node)
        self.pointers[node.id] = len(self.nodes) - 1

    # This will be O(n) because we have to check each element in the list to find the min distance
    def delete_min(self):
        min = math.inf
        minNode = self.nodes[0]
        for i in range(len(self.nodes)):
            if(self.nodes[i].distance < min):
                min = self.nodes[i].distance
                minNode = self.nodes[i]

        self.pointers[minNode.id] = -1
        for i in range(len(self.nodes)):
            if self.nodes[i].id > minNode.id:
                self.pointers[self.nodes[i].id] = self.pointers[self.nodes[i].id] - 1
        self.nodes.remove(minNode)
        return minNode

    # This will be O(1) we already have the index just have to change distance at that element
    def decrease_key(self,node_index,distance):
         self.nodes[self.pointers[node_index]].distance = distance



class Node:
    prev = 0
    distance = 0
    id = 0
    neighbors = []
    def __init__(self, prev, distance, id, neighbors):
        self.distance = distance
        self.prev = prev
        self.id = id
        self.neighbors = neighbors



class BinaryHeapPriorityQueue:

    pointers = {}
    nodes = []
    current_size = 0

    # why dont I make the pointers a map where the key is the nodeID and the value is the position in the binary
    # heap of the node its referencing
    # The complexity here will be O(logn) because we compare node distance at each level where there are logn levels
    def insert(self,node):
        self.nodes.append(node)
        self.pointers[node.id] = len(self.nodes) - 1
        i = len(self.nodes) - 1
        while(i // 2 > 0):
            if self.nodes[i].distance < self.nodes[i//2].distance:
                f = self.nodes[i]
                self.nodes[i] = self.nodes[i//2]  # child is now the parent
                self.pointers[f.id] = i // 2        # key of child now references parents position in heap
                self.pointers[self.nodes[i].id] = i   # key of parent now referenes childs position in the heap
                self.nodes[i//2] = f  # the parent is now the child
                i = i // 2
            else:
                break


    # This will be O(logn) complexity because we will compare the node to parent at each of the logn levels
    def decrease_key(self,node_index,distance):
        # want to decrease the distance of the node and then make sure it's in the appropriate position in the heap
        self.nodes[self.pointers[node_index]].distance = distance
        node = self.nodes[self.pointers[node_index]]
        i = self.pointers[node.id]
        # i is the position of the index inside of the heap
        while (i // 2 > 0):
            if self.nodes[i].distance < self.nodes[i//2].distance:
                f = self.nodes[i]
                self.nodes[i] = self.nodes[i // 2]  # child is now the parent
                self.pointers[f.id] = i // 2  # key of child now references parents position in heap
                self.pointers[self.nodes[i].id] = i  # key of parent now referenes childs position in the heap
                self.nodes[i // 2] = f  # the parent is now the child
                i = i // 2
            else:
                break

    # This is where the speed up occurs
    # The complexity here will be logn because deleting the min is constant time
    # we then compare the least node at each level which is logn time
    def delete_min(self):
        # pull of the first node and replace it with last node
        # make sure to adjust pointers when doing this
        self.current_size = self.current_size - 1
        x = self.nodes[0]
        if len(self.nodes) == 1:                                          # agbcdef
            del self.nodes[0]
            return x
        # delete the node so now its id goes to negative one in map
        self.pointers[self.nodes[0].id] = -1
        del self.nodes[0]
        last_node = self.nodes[len(self.nodes) - 1]
        self.nodes.insert(0, last_node)
        self.pointers[last_node.id] = 0
        del self.nodes[len(self.nodes) - 1]
        i = 1
        while((i * 2) + 1 <= len(self.nodes)):
            left_child = self.nodes[(i * 2) - 1]
            right_child = self.nodes[((i * 2) + 1) - 1]

            if left_child.distance < right_child.distance:
                f = self.nodes[(i * 2) - 1]
                self.pointers[last_node.id] = (i * 2) - 1
                self.nodes[(i * 2) - 1] = last_node
                self.nodes[i - 1] = f
                self.pointers[f.id] = i - 1
                i = (i * 2)
            else:
                f = self.nodes[((i * 2) + 1) - 1]
                self.pointers[last_node.id] = ((i * 2) + 1) - 1
                self.nodes[((i * 2) + 1) - 1] = last_node
                self.nodes[i - 1] = f
                self.pointers[f.id] = i - 1
                i = ((i * 2) + 1)
        return x































