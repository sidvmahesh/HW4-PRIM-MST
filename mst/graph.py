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
        #to_be_visited = [i for i in range(self.adj_mat.shape[0]) if i != start_node]
        x = self.adj_mat
        edge_heap = [(x[start_node, i], (start_node, i)) for i in np.argwhere(x[start_node] != 0).flatten()]
        mst = np.zeros_like(self.adj_mat)
        while(len(edge_heap) != 0):
            # if len(edge_heap) == 0:
            #     start_node = to_be_visited[random.randint(0, len(to_be_visited)-1)]
            #     visited = [start_node]
            #     edge_heap = [(x[start_node, i], (start_node, i)) for i in np.argwherex(x[start_node] != 0).flatten()]
            new_edge = heapq.heappop(edge_heap)
            #new_node = newly_visited_edge[1][1] if (newly_visited_edge[1][1] not in visited) else newly_visited_edge[1][0]
            new_node = new_edge[1][1]
            if new_node in visited:
                assert new_edge[1][0] in visited
                continue
            # while ((new_node in visited) and (newly_visited_edge[1][0] in visited)):
            #     if len(edge_heap) == 0:
            #         start_node = to_be_visited[random.randint(0, len(to_be_visited)-1)]
            #         visited = [start_node]
            #         edge_heap = [(x[start_node, i], (start_node, i)) for i in np.argwherex(x[start_node] != 0).flatten()]
            #     newly_visited_edge = heapq.heappop(edge_heap)
            #     #new_node = newly_visited_edge[1][1] if (newly_visited_edge[1][1] not in visited) else newly_visited_edge[1][0]
            #     new_node = newly_visited_edge[1][1]
            # new_node = newly_visited_edge[1][1] if (newly_visited_edge[1][1] not in visited) else newly_visited_edge[1][0]
            mst[new_edge[1][0], new_edge[1][1]] = new_edge[0]
            mst[new_edge[1][1], new_edge[1][0]] = new_edge[0]
            edges_to_add = [(x[new_node, i], (new_node, i)) for i in np.argwhere(x[new_node] != 0).flatten() if i not in visited]
            visited.append(new_node)
            for i in edges_to_add:
                heapq.heappush(edge_heap, i)
            # to_be_visited.remove(new_node)
        self.mst = mst
