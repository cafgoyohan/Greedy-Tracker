from Package import Package
from datetime import datetime, timedelta, date, time
import csv


class PackageHashTable:

    # Important variables for this class
    TOTAL_NUM_OF_PACKAGES = 40
    TRUCK_SPEED = 18

    # This initialization method creates the hash table
    # that will hold our packages.
    def __init__(self):
        self.packages_array = [None] * self.TOTAL_NUM_OF_PACKAGES
        self.miles = 0
        self.delivery_time = datetime.combine(date.today(), time(8, 00))
        self.package_group = []
        self.address_list = []
        self.distances_matrix = []
        self.package_group_delivered = False
        self.import_package_info()
        self.import_distance_info()

    # This method inserts the packages in our packages array
    def insert_package(self, package):
        self.packages_array[package.package_id - 1] = package

    # This method searches the hash table
    def search_package(self, package):
        if self.packages_array[package.package_id - 1] is not None:
            return self.packages_array[package.package_id-1]
        else:
            return None

    # This method returns true when all the packages
    # have been delivered, else returns false
    def all_delivered(self):
        for i in self.packages_array:
            if i.status != "Delivered":
                return False
        return True

    # This method prints out the hash table
    def print_package_hash_table(self, t):
        for i in self.packages_array:
            if t < i.time_loaded:
                i.print_package("Undelivered")
            elif i.time_loaded <= t <= i.time_delivered:
                i.print_package("Loaded on truck")
            else:
                i.print_package("Delivered")

    # This method imports the package info from the csv file 
    # into the hash table
    def import_package_info(self):
        with open('PackageDetails.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                deadline = datetime.combine(date.today(), time(int(row[4]), int(row[5])))
                delay_time = datetime.combine(date.today(), time(int(row[7]), int(row[8])))
                time_placeholder = datetime.combine(date.today(), time(1, 0))
                self.insert_package(Package(int(row[0]), row[1], row[2], int(row[3]),
                                            deadline, int(row[6]), delay_time,
                                            row[9], "Undelivered", time_placeholder, time_placeholder))
                #Appends the packages that needs to be 
                #delivered together in the package_group
                if row[9] == "y":
                    self.package_group.append(int(row[0]))

    # This method imports the distance info from the csv file
    # into the distances matrix.
    def import_distance_info(self):
        with open('PackageDistanceTable.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            count = 0
            for row in csv_reader:
                if count == 0:
                    for i in row:
                        self.address_list.append(i)
                    count += 1
                else:
                    x = []
                    for i in row:
                        x.append(float(i))
                    self.distances_matrix.append(x)

    # This is a simple function to determine if
    # the special packages that have to go together
    # can be shipped out
    def special_group(self):
        for i in self.package_group:
            if self.packages_array[i-1].delay_time < self.delivery_time:
                return False
        return True

    # Deliver function
    def deliver(self):
        # Prioritize the undelivered packages into a list
        # based on delivery deadline. This piece of code
        # also makes sure the packages that have to be
        # delivered together get delivered together.
        prioritized_list = []
        if self.special_group() and not self.package_group_delivered:
            for i in self.package_group:
                prioritized_list.append([self.packages_array[i-1].package_id, self.packages_array[i-1].deadline])
            prioritized_list.sort(key=sort_time)
            self.package_group_delivered = True
        else:
            for i in self.packages_array:
                if i.status == "Undelivered" and i.group == "n":
                    prioritized_list.append([i.package_id, i.deadline])
            prioritized_list.sort(key=sort_time)

        # Now we "load" the packages into the "truck"
        # also taking in mind the availability time
        x = 0
        truck = []
        for i in prioritized_list:
            if self.packages_array[i[0]-1].delay_time <= self.delivery_time and x <= 13:
                truck.append(i[0])
                x += 1
                self.packages_array[i[0]-1].time_loaded = self.delivery_time

        # Now comes the nearest neighbor algorithm to
        # "deliver" the packages by sorting what is
        # now on the truck according to distance.
        # This is where the Greedy Algorithm takes place
        address1 = "4001 South 700 East"
        address1_index = 0
        closest_package_id = 0
        while len(truck) > 0:
            closest = 100.0
            address1_index = self.address_list.index(address1)

            # This piece of code specifically looks for the closest package
            for i in truck:
                address2_index = self.address_list.index(self.packages_array[(i-1)].address)

                if self.distances_matrix[address1_index][address2_index] < closest:
                    closest = self.distances_matrix[address1_index][address2_index]
                    closest_package_id = i

            # Now that the closest package has been found,
            # deliver package
            self.miles += closest
            minutes = (closest / self.TRUCK_SPEED) * 60
            delta = timedelta(minutes=minutes)
            self.delivery_time += delta
            self.packages_array[closest_package_id-1].status = "Delivered"
            self.packages_array[closest_package_id - 1].time_delivered = self.delivery_time
            truck.remove(closest_package_id)
            address1 = self.packages_array[(closest_package_id-1)].address

        # Add the last trip back to hub
        address2_index = self.address_list.index("4001 South 700 East")
        closest = self.distances_matrix[address1_index][address2_index]
        self.miles += closest
        minutes = (closest / self.TRUCK_SPEED) * 60
        delta = timedelta(minutes=minutes)
        self.delivery_time += delta


# This function helps with the sort function in the
# deliver() function, and returns the second element
# in the list as a key
def sort_time(self):
    return self[1]
