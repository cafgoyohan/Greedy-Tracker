from PackageHashTable import PackageHashTable
from datetime import datetime, date, time #to work on date and time
from termcolor import colored #for colors and text layouts
import maskpass #to hide the password

# Instantiate the Package Hash Table
packages = PackageHashTable()  

#The main function
def main():
    # This while loop runs the deliver function
    # until there are no more packages to deliver
    while packages.all_delivered() is not True:
        packages.deliver()

    # When all packages have been delivered, print
    # out the results. The if statement is for these
    # print statements to run just the first time the
    # program runs.
    print(colored('\nAll the packages have been delivered!', 'green', attrs=['bold']))
    print("Time: " + str(packages.delivery_time.time()))
    print("Total miles traveled: " + str(packages.miles) + " miles" + "\n")

    # Print out prompt for user to enter time for
    # status during that time
    hr, minutes = 1, 0
    prompt = True
    while prompt:
        try:
            correct_time = False
            while not correct_time:
                print(colored('\nMonitor package status:', 'light_blue', attrs=['bold']))
                print("\nPlease enter the time from 8:00-17:00, or enter a string to exit")
                hr = int(input("Hour (8-17): "))
                if not 8 <= hr <= 17:
                    print(colored('\nPlease enter a valid hour.', 'red', attrs=['bold']))
                else:
                    minutes = int(input("Minute (0-59): "))
                    if not 0 <= minutes <= 59 or (hr == 17 and minutes != 0):
                        print(colored('\nPlease enter a valid minute.', 'red', attrs=['bold']))
                    else:
                        correct_time = True
            print("\n")
            packages.print_package_hash_table(datetime.combine(date.today(), time(hr, minutes)))

        # Once the user inputs a string, the program finally
        # ends here in the except statement.
        except ValueError:
            print(colored('\nThank you! Have a great day.\n', attrs=['bold']))
            prompt = False

#list of correct username and password
users = {'admin1': 'password1', 'admin2': 'password2', 'admin3': 'password3'}

#This runs when the username or 
#password is incorrect
def login_again():
    print(colored('\nPlease enter your credentials again.', 'green', attrs=['bold']))
    username = input("Enter your username: ")  

    #masking password with prompt msg 'Password :'
    password = maskpass.askpass("Password : ")
  
    #check if the username and password is correct
    if username in users and users[username] == password:  
        print(colored('\nLogin Successful.\n', 'green')) 
        main() #runs the main function
    else:  
        print(colored('\nInvalid username or password. Please try again.', 'red'))
        login_again()  #runs the login_again function

#This function greets the users allow
#them to log in to access the program
def login():  
    print(colored('\nWelcome! Please login to  your account.', 'green', attrs=['bold']))
    username = input("Enter your username: ")  

    #masking password with prompt msg 'Password :'
    password = maskpass.askpass("Password : ") 
  
    #check if the username and password is correct
    if username in users and users[username] == password:  
        print(colored('\nLogin Successful.\n', 'green')) 
        main() #runs the main function
    else:  
        print(colored('\nInvalid username or password. Please try again', 'red'))
        login_again()  #runs the login_again function

#The login function will be the first to run  
login()  

