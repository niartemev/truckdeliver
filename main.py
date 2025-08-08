#Student ID:012439636

import pandas as pd
import warnings
from datetime import datetime, timedelta
from Truck import Truck
from Graph import Graph, Vertex
from Package import Package
from HashTable import HashTable
from CLI import CLI
import sys

warnings.filterwarnings('ignore')

#Generate truck loads
def create_load(table):

    #Each truck can carry at most 16 packages
    max = 16

    #Initialize empty loads
    load1 = []
    load2 = []
    load3 = []

    #Loop through the hash table and load packages according to notes in the distances file. O(N)
    for i in range(1, table.size+1):
        package = table.retreive(i)
        if(len(load1) < max):
            if(package.deadline != "EOD" and str(package.notes) == "nan"):
                load1.append(i)
                package.truck = 1
                continue
            elif("Must be" in str(package.notes)):
                load1.append(i)
                package.truck = 1
                continue
            elif(i == 19):
                load1.append(i)
                package.truck = 1
                continue
            elif(i == 17):
                load3.append(i)
                package.truck = 3
                continue   
            
        if(len(load2) < max):
            if("Delayed" in str(package.notes)):
                load2.append(i)
                package.truck = 2
                continue
            elif("truck 2" in str(package.notes)):
                load2.append(i)
                package.truck = 2
                continue
        
        if(len(load3) < max/2):
            load3.append(i)
            package.truck = 3
        
        
            
    
    #Packages with notes were loaded first, another pass is needed to load the rest. O(N)
    for i in range(1, table.size+1):
        package=table.retreive(i)
        if(i in load1 or i in load2 or i in load3):
            continue
        else:
            if(len(load1)<max):
                load1.append(i)
                package.truck = 1
            else:
                load2.append(i)
                package.truck = 2
           
         
    return load1,load2,load3
    


def main():
    
    #Initialize a graph
    graph = Graph()
    dr = pd.read_csv('distances.csv', skiprows=7, nrows=27)

    #Load vertices. O(N)
    for index,row in dr.iterrows():
        graph.add_vertex(Vertex(row[1]))

    #Build adjacency lists. O(N^2)          
    counter = 0
    for vertex in graph.adjacency_list:
        counter +=1
        for index,row in dr.iterrows():
            if not (pd.isna(dr.iloc[index, counter+1])):
                graph.add_edge(vertex, graph.return_vertex(row[1]), dr.iloc[index, counter+1])
            
    #Initialize a hashtable
    table = HashTable(40)

    #Load the hashtable. O(N)
    package_reader = pd.read_csv('data.csv', skiprows=7, nrows=40, usecols=[0,1,3,4,5,6,7])
    data_index=0
    for index, row in package_reader.iterrows():  
        table.insert(Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
   

    
    #Call the load generation function
    load1,load2,load3 = create_load(table)

    #Create truck 1, set departure time, leave it at last destination
    truck1 = Truck(1,load1,table,graph)
    truck1.load_packs(datetime.strptime("8:00 AM", "%I:%M %p"))
    truck1.deliver(datetime.strptime("8:00 AM", "%I:%M %p"), return_base = False)
    
   
    #Create truck 2, instruct it to return to base
    truck2 = Truck(2,load2,table,graph)
    truck2.load_packs(datetime.strptime("9:05 AM", "%I:%M %p"))
    truck2.deliver(datetime.strptime("9:05 AM", "%I:%M %p"), return_base = True)
    
    #Update wrong address & create the last truck
    table.retreive(9).update_address(datetime.strptime("10:20 AM", "%I:%M %p"), "410 S State St")
    truck3 = Truck(3,load3,table,graph)
    truck3.load_packs(truck2.completion_time)
    truck3.deliver(truck2.completion_time, return_base = False)

    #Print delivery results
    print("All packages have been delivered.\n")

    print("Delivered by truck 1: " + str(truck1.load))
    print("Distance: " + str(truck1.distance) + "\n")
    
    print("Delivered by truck 2: " + str(truck2.load))
    print("Distance: " + str(truck2.distance) + "\n")

    print("Delivered by truck 3: " + str(truck3.load))
    print("Distance: " + str(truck3.distance) + "\n")

    #Call to interface function
    trucks = [truck1, truck2, truck3]
    CLI(table, trucks).cmdloop()
    
if __name__ == '__main__':
    main()
