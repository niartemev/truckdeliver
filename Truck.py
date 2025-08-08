from datetime import datetime, timedelta


class Truck:
    def __init__(self,id, load,table,graph):

        #Truck initializers
        self.id = id
        self.load = load
        self.distance = 0
        self.completion_time = 0
        self.departure_time = 0
        self.graph = graph
        self.table = table
        self.cur_address = "HUB"
        self.path = self.construct_path()
        
        
    def construct_path(self):

        #Intialize placeholders
        path = []
        queue = []
        current_addr = self.cur_address

        #Build a temp path
        for i in self.load:
            queue.append(i)

        #Construct a path. Nearest neighbor becomes next in the path. O(N^2)
        total = 0
        while(len(queue) != 0):
            smallest=queue[0]
            dist = self.graph.get_weight(current_addr, self.table.retreive(queue[0]).address)
            #Loop through temp que
            for i in queue:
                #If current node is closest, add it to the main path and remove it from temp path
                if ((self.graph.get_weight(current_addr, self.table.retreive(i).address) < dist)):
                    smallest = self.table.retreive(i).id
                    dist = self.graph.get_weight(current_addr, self.table.retreive(i).address)
                
            
            total+=dist
            current_addr = self.table.retreive(smallest).address
            path.append(smallest)
            queue.remove(smallest)

        #Calculate distance of a path
        def calculate_total_distance(path):
            current_addr = "HUB"
            total_distance = 0 
            for i in range(0, len(path)):
                total_distance += self.graph.get_weight(current_addr, self.table.retreive(path[i]).address)
                current_addr =  self.table.retreive(path[i]).address
                
            return total_distance

        #Store best path & best distance
        best_path = path[:]
        best_distance = calculate_total_distance(path)


        
        #(2-opt optimization, O(N^2))
        #Keep going as long as improvements are being made
        improved = True
        while improved:
            improved = False
            #Interate through the path, swap elements if it results in a cost reduction
            for i in range(0, len(path) - 1):  # We don't need to swap the last position
                for j in range(i , len(path)):
                    if j - i == 1:  # Skip adjacent points
                        continue
                    new_path = path[:]
                    # Swap the two edges
                    new_path[i:j+1] = reversed(new_path[i:j+1])
                    new_distance = calculate_total_distance(new_path)
                    
                    if new_distance < best_distance:
                        best_path = new_path
                        best_distance = new_distance
                        improved = True
                        break
                if improved:
                    break
                    
                    
        
        return best_path


    #Loading method
    def load_packs(self, time):
        for i in range(0, len(self.path)):
            package = self.table.retreive(self.path[i])
            package.status.update({time: f' Loaded on Truck {self.id}'})

        self.loaded = True
    
    #Delivery method
    def deliver(self, departure_time, return_base):

        #Check if truck is loaded
        if(self.loaded == False):
            print("Truck must be loaded prior to departure.")
            return 0

        #Store distance traveled, departure and arrival times 
        self.departure_time = departure_time
        dist = 0
        arrival_time = departure_time

        #Iterate through the path. 
        for i in range(0, len(self.path)):
                #Retreive next node. Calc distance between current and next nodes
                next = self.table.retreive(self.path[i])
                travel = self.graph.get_weight(self.cur_address, next.address)
                dist += travel
                #Calc arrival time, set current address to next
                arrival_time += timedelta(hours=(travel)/18)
                self.cur_address = next.address
                #Update package status
                next.status.update({departure_time :' En Route since'})
                next.status.update({arrival_time: ' Delivered at'})
                next.delivery_time = arrival_time
                
        #Check if truck was instructed to return home
        if(return_base == True):
            #Calc distance between last destination and HUB; add it to total
            travel = self.graph.get_weight(self.cur_address, "HUB")
            dist += travel
            arrival_time += timedelta(hours=(travel)/18)
            self.cur_address = "HUB"

        self.distance = dist
        self.completion_time = arrival_time   


        
