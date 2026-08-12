#!/usr/bin/python

# This is main program for managing the directory file.
# This version is to use with an input file.

# Programer: CG July 2026

from create_file import add_new_record
from update_drogue_file import update_drogue_off_date
from update_dead_file import update_dead_info
from update_start_file import update_start_info
from update_wmo_file import update_wmo

from helper import Menu

def return_function(choice):
    if (choice == 1):
        # This routine is used to add a new record to the directory file.
        add_new_record()
    elif (choice == 2):
        # This routine is used to change the status of the drogue in the directory file.
        update_drogue_off_date()
    elif (choice == 3):
        # This function is used to change the status of a buoy to dead in directory file.
        update_dead_info()
    elif (choice == 4):
        # This routine is used to change the start time, lat, lon of 
        # an existing record in directory file.
        update_start_info()
    elif (choice == 5):
        # This routine is used to change the start time, lat, lon of 
        # an existing record in directory file.
        update_wmo()
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            print('\n')
            print("Goodbye!" + '\n')

def main_menu():
    text = "M E N U (direp_file)"
    title = '\n' + f"{' ' * 9}{text}"  + '\n'
    title = title + f"{' ' * 9}{'=' * len(text)}"
    menu_dictionary = {
        "1. ": "to  create  new record",
        "2. ": "to update drogue information",
        "3. ": "to change buoys to dead status",
        "4. ": "to change start time, lat, lon",
        "5. ": "to change WMO numbers"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()

if __name__ == "__main__":
    main_menu()

