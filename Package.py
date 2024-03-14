from termcolor import colored
class Package:
    
    #initialization method for the package details
    def __init__(self, package_id, address, city, package_zip, deadline, weight,
                 delay_time, group, status, time_loaded, time_delivered):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.package_zip = package_zip
        self.deadline = deadline
        self.weight = weight
        self.delay_time = delay_time
        self.group = group
        self.status = status
        self.time_loaded = time_loaded
        self.time_delivered = time_delivered

    # This method simply prints out the package
    def print_package(self, status):
        if status == "Undelivered":
            print(colored(str(self.package_id) + ': ' + self.address + ', ' + self.city + ", " + str(
                self.package_zip) + ".", attrs=['underline']))
            print(colored('   Deadline: ', attrs=['bold']) + str(self.deadline.time()) + ".")
            print(colored('   Status: ', attrs=['bold']) + colored(status + ".\n", 'red', attrs=['bold']))
        elif status == "Loaded on truck":
            print(colored(str(self.package_id) + ': ' + self.address + ', ' + self.city + ", " + str(
                self.package_zip) + ".", attrs=['underline']))
            print(colored('   Deadline: ', attrs=['bold']) + str(self.deadline.time()) + ".")
            print(colored('   Status: ', attrs=['bold']) + colored(status + ".", 'yellow', attrs=['bold']))
            print(colored('   Time Loaded: ', attrs=['bold']) + str(self.time_loaded.time()) + "\n")
        else:
            print(colored(str(self.package_id) + ': ' + self.address + ', ' + self.city + ", " + str(
                self.package_zip) + ".", attrs=['underline']))
            print(colored('   Deadline: ', attrs=['bold']) + str(self.deadline.time()) + ". ")
            print(colored('   Status: ', attrs=['bold']) + colored(status + ". ", 'green', attrs=['bold']))
            print(colored('   Time Delivered: ', attrs=['bold']) + str(self.time_delivered.time()) + "\n")
