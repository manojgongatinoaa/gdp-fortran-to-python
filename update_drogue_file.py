#!/usr/bin/python

# Programer: CG July 2026

from directory_file import DirectoryFile
from file_manager import FileManager
from common import CommonFunctions

def update_drogue_off_date_in_directory_file(input_file):
#    print(*input_file, sep ='\n')
    result = None
    
    # Loads the directory file
    dirfl = DirectoryFile()
    directory_file = dirfl.rdirfl50()
    # Makes a copy of DIR-File.
    new_directory_file = directory_file.copy()

    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n')
    print("Number of DIR-File records: ", len(directory_file), '\n')

    print("Wait!: Changing drogue-off date in directory file..." + '\n')

    file = None
    file_manager = FileManager()
    input_file_path = file_manager._resolve_path(input_file)
    common = CommonFunctions()
    try:
        # input_file format: buoy id, drogue-off date.
        with open(input_file_path, "r", encoding = "utf-8") as file:
            lines = [line.rstrip() for line in file]

            print("Changed records:")

            # The loop reads a list of modified buoy information out of a raw data text file row by row.
            # For every buoy row found, it looks up where that buoy exists inside the DIR-File, prints 
            # out its old data, evaluates status overrides based on special condition flags, updates the
            # DIR-File, and writes a verification tracking statement out to the terminal.
            for line in lines:
                # split() without arguments automatically handles any consecutive whitespace
                columns = line.strip().split()
                if (len(columns) > 0): # If len(columns) == 0 the line is empty.
                    # Ensure the line has enough data to avoid IndexError
                    if (len(columns) > 1):
                        buoy_id = int(columns[0])
                        drogue_off_date = float(columns[1])
                        
                        # Looks for the ID in the DIR-File.
                        idx = common.get_id_position_in_dirfl(buoy_id, directory_file)
                        if (idx >= 0 ):
                            # Buoy ID was found in DIR-File
                            # Makes copies of DIR-File's row.
                            old_row = directory_file[idx].copy()
                            row = old_row.copy()

                            # If the given drogue_off_date = 99999 or 0 will make 
                            # drogue_off_date = end_time found in DIR-File.
                            if (int(drogue_off_date) == 99999 or int(drogue_off_date) == 0):
                                # The 8th column in DIR-File represents the date of last fix.
                                value = row[7]
                            # If the given drogue_off_date = 1 will make 
                            # drogue_off_date = start_time found in DIR-File.
                            elif (int(drogue_off_date) == 1):
                                # The 5th column in DIR-File represents the deployment date.
                                value = row[4]
                            # If the given drogue_off_date = -1 could not be determined then it will make 
                            # drogue_off_date = 1-1-1979.
                            elif (int(drogue_off_date) == -1):
                                value = 1.0 # (Julian day 1)
                            else:
                                # Make sure the given drogue-off date is not after end_time in DIR-File.
                                if (drogue_off_date > row[7]):
                                    value = row[7]
                                else:
                                    # Otherwise, it accepts the given drogue-off date.
                                    value = drogue_off_date

                            # The 15th column in DIR-File represents the drogue-off date.
                            # If the drogue-off date in DIR-File is less than or equal to 0,
                            # it indicates that the drogue was not lost.
                            row[14] = value
                            # The drogue-off date was changed?
                            if (old_row[14] != row[14]):
                                # Replace with new values.
                                new_directory_file[idx] = row

                                # Prints out a log of the buoy's parameters before any changes are applied.
                                print(f"{' ' * 4}" + f"{int(row[0])}")
                                print(f"{' ' * 6}" + "Old: drogue_off_date = " + f"{old_row[14]}" + 
                                    " start_time = " + f"{old_row[4]}" + " end_time = "+ f"{old_row[7]}")
                                # Logs the modified data to the console.
                                print(f"{' ' * 6}" + "New: drogue_off_date = " + f"{row[14]}" + 
                                    " start_time = " + f"{row[4]}" + " end_time = "+ f"{row[7]}")
                                print(' ')
                        else:
                            print(buoy_id + ": no match found in DIR-File.")
                    else:
                        print("Error: Check " + f"{input_file_path}" + " format")
                        break
    except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
    finally:
        if file:
            file.close # Always executes, ensuring the stream is freed

    if (common.compare_2D_float_lists(new_directory_file, directory_file) == False):
        result = new_directory_file
    return result

# This function is used to change the status of the drogue in the directory file (DIR_File),
# while creating a timestamped backup copy beforehand.
# It reads info from a previously created file with format: buoy id, drogue-off date.
# If drogue-off date is equal:
#     99999.99, the program assumes drogue-off date is equal last time found in DIR-File, that is used for
#               dead buoys, with drogue on until the last day.
#            1, the program assumes drogue-off date is equal start time found in DIR-File.
#           -1, the program assumes drogue-off date is equal 1, it means drogue-off date could not be determine.
def update_drogue_off_date():
    print('\n')
    print(f"{' ' * 9}{'Enter complete file name where info for records are,'}")
    input_file = str(input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/all_drogue_off.lis): '}"))

    print('\n')
    print(f"{' ' * 9}{'Expected file format: id, drogue_off_date'}")

    print('\n')
    print(f"{' ' * 9}{'Note:'}")
    print(f"{' ' * 13}{'drogue_off_date = 99999 or 0 will make drogue_off_date = end_time found in DIR-File.'}")
    print(f"{' ' * 13}{'drogue_off_date =          1 will make drogue_off_date = start_time found in DIR-File.'}")
    print(f"{' ' * 13}{'drogue_off_date =         -1 will make drogue_off_date = 1-1-1979.'}")
    
    new_directory_file = update_drogue_off_date_in_directory_file(input_file)

    if (new_directory_file != None):
        # Update the directory file
        dirfl = DirectoryFile()
        dirfl.wdirfl50(new_directory_file)
    else:
        print(f"{' ' * 4}" + "No changes")
