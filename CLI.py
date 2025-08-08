from datetime import datetime, timedelta
import cmd

#View a single package
def view_one(table):

    #Read package info
    id = input("Enter package id: ")
    time = input("Enter time in HH:MM AM/PM format: ").split(" ")
    specific = False

    #Input validation
    try:
        package = table.retreive(int(id))
        time = datetime.strptime(str(time[0]) + " " + str(time[1]), "%I:%M %p")
    
    except Exception as e:
        print("\n")
        print("You must enter a valid id and time in HH:MM AM/PM format.")
        return 0

    #Print package info
    print(package.get_status(time))
   
    
        
#View all packages within a timeframe
def view_all(table, trucks):

    time = input("Enter time in HH:MM AM/PM format: ").split(" ")

    #Validate input
    try:
        time = datetime.strptime(str(time[0]) + " " + str(time[1]), "%I:%M %p")
    except Exception as e:
        print("You must enter time in a valid format.")
        return 0

    #Print info on all packages
    for package in table.table:
        print(package.get_status(time))

    #Determine current distance
    print("\n")
    total = 0
    for truck in trucks:
        time_diff = (time - truck.departure_time).total_seconds()
        traveled = 0
        if(time <= truck.completion_time):
            if(time_diff > 0):
                time_diff = time_diff / 3600
                traveled = 18 * time_diff
            else:
                traveled = 0
        else:
            traveled = truck.distance
            
        total += traveled
        print("Truck " + str(truck.id) + " drove " + str(traveled) + " miles")

    print("Total distance traveled: " + str(total) + " miles.")

#View all deliveries 
def view_history(table, trucks):

    #Print package status at end of day
    for package in table.table:
        print(package.get_status(datetime.strptime("11:59 PM", "%I:%M %p")))
    
    #Calculate total distance. O(N)
    distance = 0
    for i in trucks:
        distance += i.distance
        
    print("\n")
    print("Truck 1 traveled " + str(trucks[0].distance) + " miles.")
    print("Truck 2 traveled " + str(trucks[1].distance) + " miles.")
    print("Truck 3 traveled " + str(trucks[2].distance)+ " miles.")
    print("Distance traveled by all trucks: " + str(distance) + " miles.")
    
#command line interface
class CLI(cmd.Cmd):

    #Instantiate CLI, table and trucks are needed to retreive package history 
    def __init__(self, table, trucks):
        super(CLI, self).__init__()
        self.table = table
        self.trucks = trucks
        
    intro = "Welcome to package tracker. The following options are available:\n1 - view status of a single package.\n2 - view status of all packages.\n3 - view delivery history and total distance.\n4 to exit."

    #Options for the user
    def do_1(self, line):
        """View status of one package"""
        view_one(self.table)

    def do_2(self, line):
        "View status of all packages"
        view_all(self.table, self.trucks)

    def do_3(self,line):
        "View complete delivery history"
        view_history(self.table, self.trucks)

    def do_4(self, line):
        """EXIT"""
        return True



        
