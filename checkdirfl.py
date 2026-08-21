#!/usr/bin/python

# Programer CG August 2026

from menu import Menu
from menu import AutoExitMenu
from database_manager import DatabaseManager
from common import CommonFunctions
from subchkdro import subchkdro
from subchkwmo import subchkwmo
from subchkdead import subchkdead
from subchkddon import subchkddon
from subchkdup import subchkdup
from subchkstet import subchkstet
from check_dirkfl import check_dirkfl
from subchkdoffkfl import subchkdoffkfl
from sub_chkspeed_dirfl50 import sub_chkspeed_dirfl50

CHANGE_DIRFL    = 1
LIST_ONLY       = 2

g_directory_file = []
g_old_directory_file = []
g_user_action = LIST_ONLY

def overwrite_return_function(choice):
    global g_user_action
    g_user_action = LIST_ONLY
    if (choice == CHANGE_DIRFL or choice == LIST_ONLY):
        # Saves the user's action choice into the global variable g_user_action.
        g_user_action = choice
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            print("Exit!" + '\n')

def overwrite_menu():
    text = "Do you want to make permanent changes to dirfl "
    text = text + "or just a listing?"
    title = '\n' + f"{' ' * 5}{text}"  + '\n'

    menu_dictionary = {
        "1. ": "change dirfl",
        "2. ": "list only"
    }
    last_option_description = "Exit"

    my_menu = AutoExitMenu(title, menu_dictionary, last_option_description, overwrite_return_function)
    my_menu.loop()

def load_dirfl():
    global g_directory_file
    if (len(g_directory_file) == 0):
        # Loads the directory file.
        # A 2D array of double-precision floating-point numbers.
        # each row with 22 columns.
        db_manager = DatabaseManager()
        g_directory_file = db_manager.select_all_dirfl()
        # Makes a copy of DIR-File.
        global g_old_directory_file
        g_old_directory_file = g_directory_file.copy()
        
        # Prints a message to the console showing how many rows were successfully loaded.
        print('\n')
        print("Number of DIR-File records: ", len(g_directory_file))

# Check drogue-off day versus starting and ending times.
def option1():
    # Loads the directory file.
    load_dirfl()
    # Asks the user if they want to overwrite the data file with fixes
    # or simply output a text report.
    overwrite_menu()
    global g_directory_file
    g_directory_file = subchkdro(g_directory_file) # external

# Check if buoys have the WMO number equal 0 which means it is not assigned.
def option2():
    # Loads the directory file.
    load_dirfl()
    # Asks the user if they want to overwrite the data file with fixes
    # or simply output a text report.
    overwrite_menu()
    global g_directory_file
    g_directory_file = subchkwmo(g_directory_file) # external

# Check if a buoy is behind in the end date and has not been declared as dead yet.
def option3():
    # Loads the directory file.
    load_dirfl()
    global g_directory_file
    subchkdead(g_directory_file) # external

# Check if a buoy is marked dead with drogue on
def option4():
    # Loads the directory file.
    load_dirfl()
    global g_directory_file
    subchkddon(g_directory_file) # external

# Check for duplicate entries in dirfl
def option5():
    # Loads the directory file.
    load_dirfl()
    global g_directory_file
    subchkdup(g_directory_file) # external

def option6():
    # check st et in dirfl against p and k sts ets
    load_dirfl()
    global g_directory_file
    subchkstet(g_directory_file) # external

def option7():
    # check if there is a k-file for each id in dirfl
    load_dirfl()
    global g_directory_file
    check_dirkfl(g_directory_file) # external

def option8():
    # check if doff in directory file is > et in kfile
    load_dirfl()
    global g_directory_file
    subchkdoffkfl(g_directory_file) # external

def option9():
    # check speed of drifters in k-file
    load_dirfl()
    global g_directory_file
    sub_chkspeed_dirfl50(g_directory_file) # external

def return_function(choice):
    # If the user selected options 3 through 9, the program automatically
    # sets g_user_action to 2 (read-only mode) because those functions do
    # not support automated corrections.
    if (choice >= 3 and choice <= 9):
        global g_user_action
        g_user_action = LIST_ONLY

    # It runs the specific diagnostic subroutine corresponding to the number
    # the user entered.
    if (choice == 1):
        # 1. check drogue off .vs. st and et
        option1()
    elif (choice == 2):
        # 2. check if a wmo has been  assigned
        option2()
    elif (choice == 3):
        # 3. to check  a buoy behind but not marked as dead
        option3()
    elif (choice == 4):
        # 4. to check if a buoy is marked dead with drogue on
        option4()
    elif (choice == 5):
        # 5. to check for duplicate entries in dirfl
        option5()
    elif (choice == 6):
        # 6. to check st et in dirfl against p and k sts ets
        option6()
    elif (choice == 7):
        # 7. to check if there is a k-file for each id in dirfl
        option7()
    elif (choice == 8):
        # 8. to check if doff in directory file is > et in kfile
        option8()
    elif (choice == 9):
        # 9. to check speed of drifters in k-file
        option9()
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        # Before it leaves checkdirfl.
        # If the user selected option 1 or 2 AND chose to save changes,
        # this calls the write subroutine wdirfl50 to save the modified
        # array back to the hard drive, and prints a success banner.
        common = CommonFunctions()
        if ((choice == 1 or choice == 2) and 
            (g_user_action == CHANGE_DIRFL) and
            (common.compare_2D_float_lists(g_old_directory_file, g_directory_file) == False)):
            # Update the DIR-File.
            db_manager = DatabaseManager()
            db_manager.update_all_dirfl(g_directory_file)

        if (choice == 0):
            print("Exit!" + '\n')

# This is a simple menu which has different options to check and optionally 
# correct the DIR-File.
def main():
    text = "M E N U (checkdirfl)"
    title = '\n' + f"{' ' * 9}{text}"  + '\n'
    title = title + f"{' ' * 9}{'=' * len(text)}"
    menu_dictionary = {
        "1. ": "to check drogue off .vs. st and et",
        "2. ": "to check if a wmo has been  assigned",
        "3. ": "to check  a buoy behind but not marked as dead",
        "4. ": "to check if a buoy is marked dead with drogue on",
        "5. ": "to check for duplicate entries in dirfl",
        "6. ": "to check st et in dirfl against p and k sts ets",
        "7. ": "to check if there is a k-file for each id in dirfl",
        "8. ": "to check if doff in directory file is > et in kfile",
        "9. ": "to check speed of drifters in k-file"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()
    
if __name__ == '__main__':
    main()