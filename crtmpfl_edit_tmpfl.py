#!/usr/bin/python

# Programer CG August 2026

# This run the option 3 from crtmpfl.py

from common import CommonFunctions
from menu import LoopMenu
from database_manager import DatabaseManager

START_TIME  = 2
END_TIME    = 3

g_idx_row = 0 # Header row

def edit_tmpfl_elemt(column, element):
    num = float(element)
    element = f"{num:.3f}"

    row = g_idx_row + 1
    db_manager = DatabaseManager()
    db_manager.change_element_tmpfl(row, column, element)

def edit_tmpfl_start_time():
    common = CommonFunctions()
    print('\n')
    start_time = input(f"{' ' * 9}{'Enter new beginning time: '}")
    if (common.is_float(start_time) == True):
        # tmpfl30.dat 3rd column represents the deployment date. 
        column = START_TIME
        edit_tmpfl_elemt(column, start_time)
    else:
        # Triggers if the user types letters, or symbols instead of a a number
        print('\n' + f"{' ' * 9}{'Invalid input! Please enter a whole number.'}")

def edit_tmpfl_last_time():
    common = CommonFunctions()
    print('\n')
    end_time = input(f"{' ' * 9}{'Enter new last day buoy had good temperature: '}")
    if (common.is_float(end_time) == True):
        # tmpfl30.dat 4th column represents the deployment date. 
        column = END_TIME
        edit_tmpfl_elemt(column, end_time)
    else:
        # Triggers if the user types letters, or symbols instead of a a number
        print('\n' + f"{' ' * 9}{'Invalid input! Please enter a whole number.'}")

def return_function(choice):
    if (choice == 1):
        edit_tmpfl_start_time()
    elif (choice == 2):
        edit_tmpfl_last_time()
    elif (choice == 3):
        edit_tmpfl()
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")       
    else:
        if (choice == 0):
            print('\n')
            print("Exit!")

# Editing an existing record in tmpfl30.dat file
def edit_tmpfl():
    # tmpfl30.dat format: Drifter ID, Experiment number, Deployment start time, Last good temperature day (end time)
    print('\n')
    input_buoy_id = input(f"{' ' * 9}{'Enter buoy ID to work with: '}")

    db_manager = DatabaseManager()
    global g_idx_row
    g_idx_row = db_manager.select_row_number_tmpfl30(input_buoy_id + ".")
    if (g_idx_row >= 0):
        # buoy ID found in tmpfl30.dat
        text = f"{input_buoy_id}{': CHANGING A RECORD'}"
        title = '\n' + f"{' ' * 9}{text}"  + '\n'
        title = title + f"{' ' * 9}{'=' * len(text)}"
        menu_dictionary = {
            "1. ": "change beginning time",
            "2. ": "change last day buoy had good temp",
            "3. ": "no more changes to this id, get next"
        }
        last_option_description = "no more changes to tmpfl30.dat"

        # I need this class to keep looping while I'm processing IDs
        # by selecting option 3.
        loop_choice = 3 # to keep processing IDs
        my_menu = LoopMenu(title, menu_dictionary, last_option_description, loop_choice, return_function)
        my_menu.loop()
    else:
        print('\n')
        print(f"Error: {input_buoy_id} not found in tmpfl30.dat, try again.")


