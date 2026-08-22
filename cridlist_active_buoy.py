#!/usr/bin/python

# Programer CG August 2026

# This run the option 2 from cridlist.py

from menu import AutoExitMenu
from database_manager import DatabaseManager
from file_manager import FileManager

ALL_SST         = 1
EXCLUDE_BAD_SST = 2

g_directory_file = []
g_active_buoys = []
g_file_name = ''

def write_list(file_name, active_buoys):
    file_manager = FileManager()
    txt_file = None
    try:
        # Write to a text file
        txt_file = file_manager.write_list('', file_name, active_buoys)
        # Prints a message to the console showing the created file.
        print('\n' + f"{'File '}{file_name}{' was created.'}" + '\n')
    except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
    finally:
        if txt_file:
            txt_file.close() # Always executes, ensuring the stream is freed

def format_output_list(buoys_list):
    output_list = []

    for row in buoys_list:
        if len(row) > 2:
            # Format: 1 starting space, a 15-character integer field, another space, 
            #         and two 9-character integer fields.
            line = ['{:>16}'.format(row[0]), '{:>10}'.format(row[1]), '{:>9}'.format(row[2])]
            output_list.append(line)

    return output_list

def get_all_active_buoys(directory_file):
    global g_active_buoys
    # The 1st column in DIR-File represents the buoy ID.
    # The 3rd column in DIR-File represents the experiment number.
    # The 4th column in DIR-File represents the buoy type classification code.
    # The 8th column in DIR-File represents the timestamp of the last successful signal fix.
    # The 22th column in DIR-File represents the death code.
    for row in directory_file:
        x = []
        death_code = int(row[21])
        end_time = row[7]
        if (death_code == 0 and end_time >= 0.0 or int(end_time) == 0):
            # The buoy is active.
            buoy_id = str(int(row[0]))
            exp_no = str(int(row[2]))
            buoy_type = str(int(row[3]))
            x.append(buoy_id)
            x.append(exp_no)
            x.append(buoy_type)
            g_active_buoys.append(x)

    # Sorting by buoy ID in ascending order
    sorted_buoy_list = sorted(g_active_buoys, key = lambda x: x[0])
    
    return sorted_buoy_list

def all_alive(directory_file):
    global g_active_buoys
    # Create all active buoys list only if it is empty.
    if len(g_active_buoys) == 0:
        g_active_buoys = get_all_active_buoys(directory_file)
    print('\n' + f"{'Total IDs active: '}{str(len(g_active_buoys))}")

    formated_list = format_output_list(g_active_buoys)
    global g_file_name
    write_list(g_file_name, formated_list)

# Filters a list of "alive" buoys.
# This receives a list of buoys and creates a new list with alive buoys with
# the temperature good to the end.
def filter_sst(active_buoys):
    sst_good_buoys = []

    print('\n' + "Wait!: Finding alive buoys with good SST from the begining...")
    db_manager = DatabaseManager()
    for row in active_buoys:
        # Get ID from alive list and check if SST good to end.
        buoy_id = row[0]
        idx = db_manager.select_row_number_tmpfl30(buoy_id + ".")
        if (idx >= 0):
            # buoy ID found in tmpfl30.dat

            # tmpfl30.dat format: id, exp_number, start_time, end_time.
            # row example: 
            # 300534068922080.   2222.   17214.625       0.000
            # If last good temperature day (end_time) is equal 0 means the temperature
            # is good to the end of the buoy's life.
            line = db_manager.select_row_tmpfl30(buoy_id)
            spl = line.split()
            if len(spl) > 3:
                start_time = int(float(spl[2]))
                end_time = int(float(spl[3]))
                if start_time != end_time:
                    # We only keep records where the temperature was valid and reliable
                    # all the way to the end of the timeline.
                    sst_good_buoys.append(row)
        else:
            print('\n')
            print(f"Error: {buoy_id} not found in tmpfl30.dat, try again.")
    
    return sst_good_buoys

# Look at SSTs, useful during the QC SST process.
# There is no need to look at those IDs that have been already identified
# as having bad SST either since the beginning or SST sensor went bad sometime
# during its trajectory.
def only_good_sst(directory_file):
    global g_active_buoys
    # Create all active buoys list only if it is empty.
    if len(g_active_buoys) == 0:
        g_active_buoys = get_all_active_buoys(directory_file)
    print('\n' + f"{'Total IDs active: '}{str(len(g_active_buoys))}")

    sst_good_buoys = filter_sst(g_active_buoys)
    print('\n' + f"{'Total IDs active with good SST: '}{str(len(sst_good_buoys))}")
    global g_file_name
    if len(sst_good_buoys) > 0:
        formated_list = format_output_list(sst_good_buoys)
        write_list(g_file_name, formated_list)
    else:
        # Prints a message to the console.
        print('\n' + f"{'File '}{g_file_name}{' was not created.'}" + '\n')
            
def sst_return_function(choice):
    global g_directory_file
    if (choice == ALL_SST):
        all_alive(g_directory_file)
    elif choice == EXCLUDE_BAD_SST:
        only_good_sst(g_directory_file)        
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            all_alive()
            print("Exit!" + '\n')

def sst_menu():
    title = '\n' + f"{' ' * 9}{'Please, select:'}"  + '\n'
    menu_dictionary = {
        "1. ": "to get alive buoys regardless the SST (all alive)",
        "2. ": "to exclude alive buoys with bad SST from the begining"
    }
    last_option_description = "Exit"

    my_menu = AutoExitMenu(title, menu_dictionary, last_option_description, sst_return_function)
    my_menu.loop()

# This function runs the option 2 from cridlist.py to create a list with all 
# active buoys.
def all_active_buoys():
    # Loads the directory file
    db_manager = DatabaseManager()
    global g_directory_file
    g_directory_file = db_manager.select_all_dirfl()

    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n')
    print(f"{'Number of DIR-File records: '}{len(g_directory_file)}" + '\n')
    
    print(f"{' ' * 9}{'Enter the complete output file name to be created,'}")
    global g_file_name
    g_file_name = input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/allalive.lis): '}")

    # Asks the user if they want to include all alive buoys or
    # only these with good SST from the beginning.
    sst_menu()

