#!/usr/bin/python

# Programer CG August 2026

from menu import Menu
from database_manager import DatabaseManager
from verify import verify
from list_by_experiment_menu import list_by_experiment_menu
from list_all_buoys_menu import list_all_buoys_menu

g_jd_to_date = False
g_created_files = []
g_count = 50

# To list a single record.
def list_by_id():
    db_manager = DatabaseManager()
    # Loads the directory filed
    directory_file = db_manager.select_all_dirfl()

    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n')
    print("Number of DIR-File records: ", len(directory_file))

    print('\n')
    buoy_id = input(f"{' ' * 9}{'Enter buoy ID to work with: '}")

    # Looks for the ID in the DIR-File.
    db_manager = DatabaseManager()
    idx = db_manager.select_row_number_dirfl(int(buoy_id))
    if (idx >= 0 ):
        # Buoy ID was found in DIR-File
        row = directory_file[idx].copy()
        change_record = False
        verify(row, g_jd_to_date, change_record)
    else:
        print('\n')
        print(buoy_id + ": no match found in DIR-File.")

def return_function(choice):
    global g_count
    if (choice == 1):
        # This is an internal function which list a single record.
        # It calls the verify() function in verify.py.
        list_by_id()
    elif (choice == 2):
        # Reassign the returned value to the original variable
        g_count = list_by_experiment_menu(g_jd_to_date, g_count, g_created_files) # external
    elif (choice == 3):
        # Reassign the returned value to the original variable
        g_count = list_all_buoys_menu(g_jd_to_date, g_count, g_created_files) # external
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            # Before it leaves inventory_menu().
            if (len(g_created_files) > 0):
                # Modifies the list (In-place)
                g_created_files.sort()
                # Prints a message to the console showing how many
                # files were successfully created.
                print('\n')
                print("The following file(s) have been created:")
                for file_name in g_created_files:
                    print(f"{' ' * 5}{file_name}")
                print("You can print or look at them now.")
                print("Each line contains 131 characters.")

            print('\n')
            print("Exit!" + '\n')

# This menu lists the DIR-File record for a given ID.
# Alternatively, it can create a file listing all buoys by experiment number
# or listing all buoys regardless of experiment number.
# Parameter:
#   jd_to_date     - Flag controlling date formatting. If True, timestamps convert 
#                    to Month/Day/Year. If False, they print as raw decimals.
def inventory_menu(jd_to_date):
    global g_jd_to_date
    g_jd_to_date = jd_to_date

    text = "M E N U (inventory)"
    title = '\n' + f"{' ' * 9}{text}"  + '\n'
    title = title + f"{' ' * 9}{'=' * len(text)}"
    menu_dictionary = {
        "1. ": "l i s t   by  i d  on terminal",
        "2. ": "create file and/or list by experiment #",
        "3. ": "create file and/or list all buoys"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()
