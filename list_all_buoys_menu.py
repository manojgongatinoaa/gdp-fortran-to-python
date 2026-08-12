#!/usr/bin/python

# Programer CG August 2026

from pathlib import Path

from database_manager import DatabaseManager
from file_manager import FileManager
from helper import Menu
from direp_print import dprint_active
from direp_print import dprint_dead
from direp_print import dprint_all

g_directory_file = []
g_jd_to_date = False
g_created_files = []
g_destination_directory = ''
g_count = 0

def load_dirfl():
    global g_directory_file
    if (len(g_directory_file) == 0):
        # Loads the directory file
        db_manager = DatabaseManager()
        g_directory_file = db_manager.select_all_dirfl()
        # Sort the 2D list in place by the first element (index 0)
        g_directory_file.sort(key = lambda x: x[0])

        # Prints a message to the console showing how many rows were successfully loaded.
        print('\n')
        print("Number of DIR-File records: ", len(g_directory_file))

def enter_destination_path():
    print('\n')
    print(f"{' ' * 9}{'Enter directory where the files for05*.dat will go,'}")
    global g_destination_directory
    g_destination_directory = input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/): '}")
    # Check if the last character is not a slash.
    if ((g_destination_directory) and (not g_destination_directory.endswith('/'))):
        g_destination_directory += "/"

def write_file(file_for05X):
    if len(file_for05X) > 0:
        global g_count
        g_count += 1
        overwrite = True
        while True:
            file_name = f"{'for0'}{g_count}{'.dat'}"
            print('\n' + "Wait!: File " + file_name + " has been created...")
            file_path = f"{g_destination_directory}{file_name}"

            path = Path(file_path)
            # Check if the path exists (can be a file OR a directory)
            if path.exists():
                answer = input(f"{' ' * 9}{'overwrite '}{file_path}{' ? '}")
                if (answer.upper() == 'Y'):
                    overwrite = True
                else:
                    overwrite = False
                    g_count += 1
            else:
                overwrite = True

            if overwrite:
                # WRITE FILE
                fl_manager = FileManager()
                fl_manager.write_list('', file_path, file_for05X)
                global g_created_files
                g_created_files.append(file_name)
                break

def active_buoys():
    # Creates for05*.dat file
    global g_directory_file
    # Formats and writes records
    file_for05X = dprint_active(g_directory_file, g_jd_to_date)
    write_file(file_for05X)

def dead_buoys():
    # Creates for05*.dat file
    global g_directory_file
    # Formats and writes records
    file_for05X = dprint_dead(g_directory_file, g_jd_to_date)
    write_file(file_for05X)
    
def all_buoys():
    # Creates for05*.dat file
    global g_directory_file
    # Formats and writes records
    file_for05X = dprint_all(g_directory_file, g_jd_to_date)
    write_file(file_for05X)

# Prints out to screen file just written
def Display_created_files():
    fl_manager = FileManager()
    for file_name in g_created_files:
        file_path = Path(file_name)
        # Check if the path exists (can be a file OR a directory)
        if file_path.exists():
            print(fl_manager.read_text(file_name))
    
def return_function(choice):
    if (choice == 1):
        # 1. a c t i v e  buoys
        active_buoys() # create file for05*.dat
    elif (choice == 2):
        # 2. d e a d  buoys
        dead_buoys() # create file for05*.dat
    elif (choice == 3):
        # 3. a l l  buoys
        all_buoys() # create file for05*.dat
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            if (len(g_created_files) > 0):
                # Before it leaves list_by_experiment_menu().
                print('\n')
                answer = input(f"{' ' * 9}{'Do you want to display the created files on the screen? (y/n)' }")
                if (answer.upper() == 'Y'):
                    Display_created_files()

            print('\n')
            print("Exit!" + '\n')

# This menu lists DIR-File records for active, dead or all buoys.
# It creates a file listing buoys regardless of experiment number.
# Alternatively, it can display the list in the terminal.
# Parameter:
#   jd_to_date     - Flag controlling date formatting. If True, timestamps convert 
#                    to Month/Day/Year. If False, they print as raw decimals.
#   count          - A counter tracking how many output reports have been generated
#                    during the execution session.
#   created_files  - List of file's path just written.
def list_all_buoys_menu(jd_to_date, count, created_files) -> int:
    load_dirfl()
    enter_destination_path()
    global g_jd_to_date
    g_jd_to_date = jd_to_date
    global g_count
    g_count = count
    global g_created_files
    g_created_files = created_files
    
    text = "M E N U (all buoys regardless of experiment number)"
    title = '\n' + f"{' ' * 9}{text}"  + '\n'
    title = title + f"{' ' * 9}{'=' * len(text)}"
    menu_dictionary = {
        "1. ": "a c t i v e  buoys",
        "2. ": "d e a d  buoys",
        "3. ": "a l l  buoys"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()

    # Send the changed value back
    return g_count
