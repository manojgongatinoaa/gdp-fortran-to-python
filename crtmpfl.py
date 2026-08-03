#!/usr/bin/python

# Here's a simple Python menu using the 'input()' function to run various commands:

# Programer: CG August 2026

from crtmpfl_update_tmpfl import update_tmpfl
from crtmpfl_edit_tmpfl import edit_tmpfl
from helper import Menu

def create_tmpfl():
    print('\n' + "You need administrator privileges.")

def return_function(choice):
    if (choice == 1):
        create_tmpfl()
    elif (choice == 2):
        update_tmpfl()
    elif (choice == 3):
        edit_tmpfl()
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")       
    else:
        if (choice == 0):
            print('\n')
            print("Exit!")

# This manages a database file (tmpfl30.dat) that tracks drifter buoys,
# recording their identification number, experiment number, deployment time,
# and the last date they reported valid temperature data.
# It allows the user to back up the data, initialize a new file, append new drifter 
# records, or manually update the temperature failure dates for specific buoys.    
def crtmpfl30_main_menu():
    title = '\n' + f"{' ' * 9}{'M E N U (crtmpfl)'}"  + '\n'
    title = title + f"{' ' * 9}{'=========================='}"
    menu_dictionary = {
        "1. ": "if this is to create a file for first time",
        "2. ": "if this is an update",
        "3. ": "if this is to make a change to existing record"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()

if __name__ == "__main__":
    crtmpfl30_main_menu()

