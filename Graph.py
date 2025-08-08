#Vertex class contains an addresses 
class Vertex:
    def __init__(self, address):
        self.address = address
    
    
#Graph
class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}
        
    #Add a vertex    
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    #Add an edge, weight is distance
    def add_full_edge(self, from_vertex, to_vertex, weight):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        if to_vertex not in self.adjacency_list[from_vertex]:
            self.adjacency_list[from_vertex].append(to_vertex)
            
    #Call to add edges twice to ensure symmetry 
    def add_edge(self, vertex_a, vertex_b, weight):
        self.add_full_edge(vertex_a, vertex_b, weight)
        self.add_full_edge(vertex_b, vertex_a, weight)

    #Return edge weight 
    def get_weight(self, address_a, address_b):

        vertex_a = self.return_vertex(address_a)
        vertex_b = self.return_vertex(address_b)
        
        return self.edge_weights[vertex_a, vertex_b]
    
    #Given an address, return a vertex  
    def return_vertex(self, address):
        for i in self.adjacency_list:
            if(address[:5] in i.address):
                return i
            
