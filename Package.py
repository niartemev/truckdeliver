from datetime import datetime

BOD = datetime.strptime("12:00 AM", "%I:%M %p")

#Package object
class Package:
    def __init__(self, id, address, city, zip, deadline, weight, notes):
        self.id = id
        self.address = address
        self.city = city
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = {}
        self.truck = 0
        self.delivery_time = 0
        self.status_init()
        
        
    #Sets initial status
    def status_init(self):
        value = 0
        if ("Delayed" in str(self.notes)):
            value="Delayed on flight"
        else:
            value = "At the hub"
        time = BOD
        self.status.update({time : value})

    #Retreive package information 
    def get_status(self, time):

        index = time
        status = self.status.get(BOD)
        address = self.address

        #Iterate through status history
        for key, value in self.status.items():
            tmp = key.replace(second=0, microsecond=0)
            #Find correct timestamp
            if(tmp <= time):
                if("Updated" not in str(value)):
                    index = tmp
                    status = value
            elif(tmp >= time):
                if("Updated" in str(value)):
                    address = str(value)[21:]
                

        #Time formatting to avoid redundancy
        reference_time = 0
        if(index == BOD):
            reference_time = ""
        else:
            reference_time = datetime.strftime(index, "%I:%M %p")
        
        return "Package #" + str(self.id) + "| Address:" + address + "| Deadline: " + self.deadline + "| Truck " + str(self.truck) + "| " + str(status) + " " + reference_time

                
            
    #Method to update address and record previous one
    def update_address(self, time, new_address):

        self.status.update({time : f'Updated address from {self.address}'})
        self.address = new_address

        
        
