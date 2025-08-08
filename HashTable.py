from Package import Package

#Hash table implementation
class HashTable:
    def __init__(self, capacity=40):
        #Initialize a table & build an array of empty packages
        self.table = []
        self.size = capacity
        for i in range(capacity):
            self.table.append(Package)
            
    #Insert by id
    def insert(self, item):
        bucket = hash(item.id) % len(self.table)
        self.table[bucket] = item
        
    #Retreive by id
    def retreive(self, id):
        if(id not in range(1, self.size+1)):
            raise Exception("Invalid id.")
            
        bucket = hash(id) % len(self.table)
        return self.table[bucket]
    
