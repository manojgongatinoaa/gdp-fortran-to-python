#!/usr/bin/python

# Here's a simple Python menu using the 'input()' function to run various commands:
# Each option create a list of ids, reading the DIR-File (dirfl)

# Programer: CG July 2026

import os
from cridlist_option5 import option_5
from helper import Menu

def option_1():
    print("You selected Option 1.")
    # Add your command logic here for Option 1

def option_2():
    print("You selected Option 2.")
    # Add your command logic here for Option 2

def option_3():
    print("You selected Option 3.")
    # Add your command logic here for Option 3

def option_4():
    print("You selected Option 4.")
    # Add your command logic here for Option 4

def return_function(choice):
    if (abs(choice) == 5):
        option_5(choice)
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")       
    else:
        if (choice == 0):
            print('\n')
            print("Exit!")
    
def cridlist_main_menu():
    title = '\n' + f"{' ' * 9}{'M E N U (function crdlist)'}"  + '\n'
    title = title + f"{' ' * 9}{'=========================='}"
    menu_dictionary = {
        "1. ": "Option 1",
        "2. ": "Option 2",
        "3. ": "Option 3",
        "4. ": "Option 4",
        "5. ": "All active buoys with drogue ON (-5 = with drogue OFF)" + '\n' + f"{' ' * 13}{'separated by manufacturer if needed'}"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()

if __name__ == "__main__":
    cridlist_main_menu()

