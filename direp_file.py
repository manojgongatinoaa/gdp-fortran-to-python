#!/usr/bin/python

# This is main program for managing the directory file.
# This version is to use with an input file.

# Programer: CG July 2026

from update_drogue_file import update_drogue_off_date
from update_dead_file import update_dead_info
from create_file import add_new_record
from helper import Menu

def return_function(choice):
    if (choice == 1):
        add_new_record()
    elif (choice == 2):
        # This routine is used to change the status of the drogue in the directory file.
        update_drogue_off_date()
    elif (choice == 3):
        # This function is used to change the status of a buoy to dead in directory file.
        update_dead_info()
    elif (choice == 4):
        print('\n' + f"{' ' * 9}{'*** To do ***'}")
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            print('\n')
            print("Goodbye!" + '\n')

def main_menu():
    title = '\n' + f"{' ' * 9}{'M E N U (direp_file)'}"  + '\n'
    title = title + f"{' ' * 9}{'=========================='}"
    menu_dictionary = {
        "1. ": "to  create  new record",
        "2. ": "to update drogue information",
        "3. ": "to change buoys to dead status",
        "4. ": "to change start time, lat, lon (under construction - Ibis)"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()

if __name__ == "__main__":
    main_menu()

