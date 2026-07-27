#!/usr/bin/python

# Programer: CG July 2026

# Here's a simple Python menu using the 'input()' function to run various commands:
# Each option create a list of ids, reading the DIR-File (dirfl)

import os
from directory_file import rdirfl50
from buoy_drogue import drogue
from helper import Menu

# Parameters:
# buoy_list -         The incoming data array containing buoy properties. 
#                     First column is the ID, second column is the program, 
#                     and the third column is the buoy type.
# output_files_path - A character string containing the root directory path
#                     or for the output files.
def byman(buoy_list, output_files_path):
    # This function receives a list of IDs and creates individual text files separated by their manufacturer.
    # It loops through each buoy ID, looks up its configuration details via external tracking databases,
    # matches it to a manufacturer code, and logs its coordinates.

    for row in buoy_list:
        found = False
        # Find out which manufacturer built this buoy.
        # 15-digit ID
        buoy_id = row[0]

        # If not found, it falls back to a 6-digit ID.
        if (not found):
            print("ID: " + str(buoy_id) + " not found")
    
    print('\n' + "The following files have been created:")
    print(f"{' ' * 5}{output_files_path}")
    

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

def separate_by_manufacture(drogue_list_path, sorted_list):
    while True:
        print('\n' + f"{' ' * 9}{'enter: 1. to create separate files with ids by manufacturer'}")
        print(f"{' ' * 16}{'0. to return'}")
        try:
            # The input() function always returns a string
            option = int(input('\n' + f"{' ' * 9}{'Enter your choice (0-1): '}"))
            if option == 1:
                # Creates separate files with IDs by manufacturer.
                files_path = os.path.dirname(os.path.abspath(drogue_list_path))
                byman(sorted_list, files_path)
            elif option == 0:
                print('\n' + f"{' ' * 9}{'Return!'}")
                break
            else:
                print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
        except ValueError as e:
            # Triggers if the user types letters, symbols, or floats instead of an integer
            ('\n' + f"{' ' * 9}{'Invalid input! Please enter a whole number.'}")

def option_5(choice):
    txt = ''
    if choice == 5:
        txt = "ON"
    else:
        txt = "OFF"
        
    # Loads the directory file
    directory_file = rdirfl50()

    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n', "Number of DIR-File records: ", len(directory_file), '\n')
    
    print(f"{' ' * 9}{'Enter the complete output file name to be created,'}")
    drogue_list_path = str(input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/drogues.lis): '}"))

    # Filters the buoys based on whether the drogue is ON or OFF
    gdt = 0.0 # all buoys anyways
    buoy_list = drogue(choice, gdt, directory_file) # Result list format: buoy_id, program_number, buoy_type
    # Sorting by buoy id in ascending order
    sorted_list= sorted(buoy_list, key = lambda x: x[0])

    # Prints a message to the console showing how many buoys have the drogue ON or OFF.
    print('\n', "Number of buoys with drogue " + txt + ": ", len(sorted_list), '\n')

    try:
        txt_file = None
        # Write to a text file
        with open(drogue_list_path, "w") as txt_file:
            for row in sorted_list:
                # Convert each element to string, join with tabs, and add a newline
                line = '\t'.join(str(item) for item in row)
                txt_file.write(line + '\n')
    except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
    finally:
        if txt_file:
            txt_file.close # Always executes, ensuring the stream is freed

    separate_by_manufacture(drogue_list_path, sorted_list)            

def option_function(choice):
    if (abs(choice) == 5):
        option_5(choice)
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")       
    else:
        if (choice == 0):
            print('\n' + f"{' ' * 9}{'Exit!'}")
    
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

    my_menu = Menu(title, menu_dictionary, last_option_description, option_function)
    my_menu.loop()

if __name__ == "__main__":
    cridlist_main_menu()

