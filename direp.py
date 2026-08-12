#!/usr/bin/python

# Here's a simple Python menu using the 'input()' function to run various commands:

# Programer: CG August 2026

from helper import Menu
from to_list import to_list
from change import change
from create import create
from buoystat import buoystat

def return_function(choice):
    # Check the sign of the choice.
    jd_to_date = False
    if (choice > 0):
        jd_to_date = True

    if (abs(choice) == 1):
        # Selected: 1. l i s t      buoys
        to_list(jd_to_date)
    elif (abs(choice) == 2):
        # Selected: 2. c r e a t e  record
        create(jd_to_date)
    elif (abs(choice) == 3):
        # Selected: 3. c h a n g e  record
        # Check the sign of the choice.
        change(jd_to_date, True)
    elif (abs(choice) == 4):
        # Selected: 4. s t a t i s t i c s
        buoystat(jd_to_date)
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            print('\n')
            print("Goodbye!" + '\n')

# This is a main program for the DIR-File.
# It acts as an interactive menu-driven interface to add, modify, list, 
# or compute statistics on buoy records stored in the DIR-File file.
def main():
    text = "M E N U (direp)"
    title = '\n' + f"{' ' * 9}{text}"  + '\n'
    title = title + f"{' ' * 9}{'=' * len(text)}" + '\n'
    title = title + f"{' ' * 5}{'(negative selection means julian date)'}"
    menu_dictionary = {
        "1. ": "l i s t      buoys",
        "2. ": "c r e a t e  record",
        "3. ": "c h a n g e  record",
        "4. ": "s t a t i s t i c s"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()

if __name__ == '__main__':
    main()
