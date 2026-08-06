#!/usr/bin/python

# Programer CG July 2026

# This run the option 5 from cridlist.py

import os

from buoy_drogue import BuoyDrogue
from directory_file import DirectoryFile
from file_manager import FileManager
from database_manager import DatabaseManager

# This function receives a list of IDs and creates individual text files
# separated by their manufacturer.
# Parameters:
# buoy_list -         The incoming data array containing buoy properties. 
#                     First column is the ID, second column is the experiment_number, 
#                     and the third column is the buoy type.
# output_files_path - A character string containing the root directory path
#                     or for the output files.
def byman(buoy_list, output_files_path):
    if ((output_files_path) and (not output_files_path.endswith('/'))):
            output_files_path += "/"
    
    # Manufacturer identification code:
    #     1 - Clearwater
    #     2 - Technocean
    #     3 - Metocean
    #     7 - Marlin-yug
    #     9 - Pac gyre
    #    11 - Dbi
    #    12 - SIO
    #    13 - Nke
    #    99 - Others
    manufacturer_dictionary = {
        "1": "drogues_clearwater.lis",
        "2": "drogues_technocean.lis",
        "3": "drogues_metocean.lis",
        "7": "drogues_marlin.lis",
        "9": "drogues_pacgyre.lis",
        "11": "drogues_dbi.lis",
        "12": "drogues_sio.lis",
        "13": "drogues_nke.lis",
        "99": "drogues_others.lis",
        "998": "drogues_unknown_code.lis",
        "999": "drogues_unknown_manufacturer.lis"
    }
    clearwater = []
    technocean = []
    metocean = []
    marlin = []
    pacgyre = []
    sio = []
    dbi = []
    nke = []
    others = []
    unknown_code = []
    unknown_manufacture = []

    db_manager = DatabaseManager()
    # Loading the entire file into memory once.
    matrix = db_manager.select_buoy_manufacturer()
    #print(*matrix, sep="\n")

    # It loops through each buoy ID.
    for row in buoy_list:
        # Find out which manufacturer built this buoy.
        buoy_id = str(row[0])

        id_found = False
        manufacturer = None
        # The main reason why the loop is so slow is that on every pass, 
        # the CPython interpreter is doing some extra work that wastes time.
        for i in range(len(matrix)):
            # Checks if the target ID equals the stored ID.
            if matrix[i][0] == buoy_id:
                # If a match is found extract the manufacturer
                manufacturer = matrix[i][1]
                id_found = True
                break

        experiment_number = str(row[1])
        buoy_type = str(row[2])
        if id_found == True:
            # Format: 1 starting space, a 15-character integer field, another space, 
            #         and three 9-character integer fields.
            line = ['{:>16}'.format(str(buoy_id)), '{:>10}'.format(str(experiment_number)), '{:>9}'.format(str(buoy_type)), '{:>9}'.format(str(manufacturer))]

            if (manufacturer == '1'):
                clearwater.append(line)
            elif (manufacturer == '2'):
                technocean.append(line)
            elif (manufacturer == '3'):
                metocean.append(line)
            elif (manufacturer == '7'):
                marlin.append(line)
            elif (manufacturer == '9'):
                pacgyre.append(line)
            elif (manufacturer == '11'):
                dbi.append(line)
            elif (manufacturer == '12'):
                sio.append(line)
            elif (manufacturer == '13'):
                nke.append(line)
            elif (manufacturer == '99'):
                others.append(line)
            else:
                # ID is known but the manufacturer doesn't match predefined codes
                unknown_code.append(line)
        else:
            # buoy_id not found in /phodnet/drifter/data/files/tpb_ab_coef15.dat
            line = ['{:>16}'.format(str(buoy_id)), '{:>10}'.format(str(experiment_number)), '{:>9}'.format(str(buoy_type))]
            unknown_manufacture.append(line)
    
    if (len(clearwater) > 0 or len(technocean) > 0 or len(metocean) > 0 or
        len(marlin) > 0 or len(pacgyre) > 0 or len(sio) > 0 or
        len(dbi) > 0 or len(nke) > 0 or len(others) > 0 or len(unknown_code) > 0 or
        len(unknown_manufacture) > 0):
        print('\n')
        print("The following file(s) have been created:")

    # Creates output files  and save them
    file_manager = FileManager()
    file_name = ''
    try:
        if (len(clearwater) > 0):
            file_name = manufacturer_dictionary['1']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", clearwater)
            print(f"{' ' * 9}{file_name}")
        if (len(technocean) > 0):
            file_name = manufacturer_dictionary['2']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", technocean)
            print(f"{' ' * 9}{file_name}")
        if (len(metocean) > 0):
            file_name = manufacturer_dictionary['3']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", metocean)
            print(f"{' ' * 9}{file_name}")
        if (len(marlin) > 0):
            file_name = manufacturer_dictionary['7']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", marlin)
            print(f"{' ' * 9}{file_name}")
        if (len(pacgyre) > 0):
            file_name = manufacturer_dictionary['9']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", pacgyre)
            print(f"{' ' * 9}{file_name}")
        if (len(dbi) > 0):
            file_name = manufacturer_dictionary['11']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", dbi)
            print(f"{' ' * 9}{file_name}")
        if (len(sio) > 0):
            file_name = manufacturer_dictionary['12']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", sio)
            print(f"{' ' * 9}{file_name}")
        if (len(nke) > 0):
            file_name = manufacturer_dictionary['13']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", nke)
            print(f"{' ' * 9}{file_name}")
        if (len(others) > 0):
            file_name = manufacturer_dictionary['99']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", others)
            print(f"{' ' * 9}{file_name}")
        if (len(unknown_code) > 0):
            file_name = manufacturer_dictionary['998']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", unknown_code)
            print(f"{' ' * 9}{file_name}")
        if (len(unknown_manufacture) > 0):
            file_name = manufacturer_dictionary['999']
            txt_file = file_manager.write_list('', f"{output_files_path}{file_name}", unknown_manufacture)
            print(f"{' ' * 9}{file_name}")
    except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
    finally:
        if txt_file:
            txt_file.close # Always executes, ensuring the stream is freed

# This function creates separate files with IDs by manufacturer
# Parameters:
# drogues_lis      - The complete output file name created with all Ids before separation.
# sorted_buoy_list - The incoming data array containing buoy properties. 
#                    First column is the ID, second column is the experiment_number, 
#                    and the third column is the buoy type.
def separate_by_manufacture(drogues_lis, sorted_buoy_list):
    while True:
        print(f"{' ' * 9}{'1. to create separate files with ids by manufacturer'}")
        print(f"{' ' * 9}{'0. to return'}")
        try:
            # The input() function always returns a string
            option = int(input('\n' + f"{' ' * 9}{'Enter your choice (0-1): '}"))
            if option == 1:
                # Creates separate files with IDs by manufacturer.
                files_path = os.path.dirname(os.path.abspath(drogues_lis))
                print('\n')
                print(f"{'Wait!: Separating files by manufacturer...'}" + '\n')
                byman(sorted_buoy_list, files_path)
                print("Ready!")
            elif option == 0:
                print('\n')
                print("Return!")
                break
            else:
                print('\n')
                print(f"{' ' * 9}{'Invalid choice! Please try again.'}")
        except ValueError as e:
            # Triggers if the user types letters, symbols, or floats instead of an integer
            ('\n' + f"{' ' * 9}{'Invalid input! Please enter a whole number.'}")

# This function runs the option 5 from cridlist.py to create a list with all 
# active buoys with drogue ON or OFF and separated by manufacturer if needed.
def according_drogue_status(choice):
    txt = ''
    if choice == 5:
        txt = "ON"
    else:
        txt = "OFF"
        
    # Loads the directory file
    dirfl = DirectoryFile()
    directory_file = dirfl.rdirfl50()

    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n')
    print(f"{'Number of DIR-File records: '}{len(directory_file)}" + '\n')
    
    print(f"{' ' * 9}{'Enter the complete output file name to be created,'}")
    drogues_lis = input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/drogues.lis): '}")

    gdt = 0.0 # all buoys anyways
    buoy_drogue = BuoyDrogue(directory_file, gdt)
    # Filters the buoys based on whether the drogue is ON or OFF
    buoy_list = buoy_drogue.drogue(choice) # Result list format: buoy_id, experiment_number, buoy_type
    # Sorting by buoy ID in ascending order
    sorted_buoy_list= sorted(buoy_list, key = lambda x: x[0])

    # Prints a message to the console showing how many buoys have the drogue ON or OFF.
    print('\n')
    print(f"{'Number of buoys with drogue '}{txt}{': '}{len(sorted_buoy_list)}" + '\n')

    formatted_line = []
    for row in sorted_buoy_list:
        # Format: 1 starting space, a 15-character integer field, 
        #         another space, and two 9-character integer fields).
        line = ['{:>16}'.format(str(row[0])), '{:>10}'.format(str(row[1])), '{:>9}'.format(str(row[2]))]        
        formatted_line.append(line)

    file_manager = FileManager()
    try:
        # Write to a text file
        txt_file = file_manager.write_list('', drogues_lis, formatted_line)
        # Prints a message to the console showing the created file.
        print(f"{'File '}{drogues_lis}{' was created.'}" + '\n')
    except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
    finally:
        if txt_file:
            txt_file.close # Always executes, ensuring the stream is freed

    # After loading the ID list found in DIR-File and filtering
    # the buoys based on whether the drogue is ON or OFF
    # we have to create separate files with IDs by manufacturer
    separate_by_manufacture(drogues_lis, sorted_buoy_list)            


