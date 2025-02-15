import numpy as np
import heapq
from typing import Union
import random

class Graph:

    def __init__(self, adjacency_mat: Union[np.ndarray, str]):
        """
    
        Unlike the BFS assignment, this Graph class takes an adjacency matrix as input. `adjacency_mat` 
        can either be a 2D numpy array of floats or a path to a CSV file containing a 2D numpy array of floats.

        In this project, we will assume `adjacency_mat` corresponds to the adjacency matrix of an undirected graph.
    
        """
        if type(adjacency_mat) == str:
            self.adj_mat = self._load_adjacency_matrix_from_csv(adjacency_mat)
        elif type(adjacency_mat) == np.ndarray:
            self.adj_mat = adjacency_mat
        else: 
            raise TypeError('Input must be a valid path or an adjacency matrix')
        self.mst = None

    def _load_adjacency_matrix_from_csv(self, path: str) -> np.ndarray:
        with open(path) as f:
            return np.loadtxt(f, delimiter=',')

    def construct_mst(self):
        """
    
        TODO: Given `self.adj_mat`, the adjacency matrix of a connected undirected graph, implement Prim's 
        algorithm to construct an adjacency matrix encoding the minimum spanning tree of `self.adj_mat`. 
            
        `self.adj_mat` is a 2D numpy array of floats. Note that because we assume our input graph is
        undirected, `self.adj_mat` is symmetric. Row i and column j represents the edge weight between
        vertex i and vertex j. An edge weight of zero indicates that no edge exists. 
        
        This function does not return anything. Instead, store the adjacency matrix representation
        of the minimum spanning tree of `self.adj_mat` in `self.mst`. We highly encourage the
        use of priority queues in your implementation. Refer to the heapq module, particularly the 
        `heapify`, `heappop`, and `heappush` functions.

        """
        start_node = random.randint(0, self.adj_mat.shape[0] - 1)
        visited = [start_node]
        x = self.adj_mat # Just for simpler reference downstream
        edge_heap = [(x[start_node, i], start_node, i) for i in np.argwhere(x[start_node] != 0).flatten()]
        heapq.heapify(edge_heap) # Transform the unsorted list to a heap
        mst = np.zeros_like(self.adj_mat)
        while(len(edge_heap) != 0):
            new_edge = heapq.heappop(edge_heap)
            new_node = new_edge[2]
            if new_node in visited:
                continue # We shouldn't add edges between two nodes already in the mst
            mst[new_edge[1], new_edge[2]] = new_edge[0]
            mst[new_edge[2], new_edge[1]] = new_edge[0]
            edges_to_add = [(x[new_node, i], new_node, i) for i in np.argwhere(x[new_node] != 0).flatten()]
            visited.append(new_node)
            for i in edges_to_add:
                heapq.heappush(edge_heap, i)
        self.mst = mst
