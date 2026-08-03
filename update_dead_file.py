#!/usr/bin/python

# Programer: CG July 2026

from directory_file import DirectoryFile
from file_manager import FileManager
from common import CommonFunctions

def update_dead_info_in_directory_file(input_file):
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

    print("Wait!: Changing dead time, dead position and dead code in directory file..." + '\n')

    file = None
    file_manager = FileManager()
    input_file_path = file_manager._resolve_path(input_file)
    common = CommonFunctions()
    try:
        # input_file format: buoy id, dead time, dead latitude, dead longitude, dead code.
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
                    if (len(columns) > 4):
                        buoy_id         = int(columns[0])
                        death_time      = float(columns[1])
                        death_latitude  = float(columns[2])
                        death_longitude = float(columns[3])
                        death_code      = float(columns[4])
                        
                        # Looks for the ID in the DIR-File.
                        idx = common.get_id_position_in_dirfl(buoy_id, directory_file)
                        if (idx >= 0 ):
                            # Buoy ID was found in DIR-File
                            # Makes copies of DIR-File's row.
                            old_row = directory_file[idx].copy()
                            row = old_row.copy()

                            # If death_time, death_latitude and death_longitude are equal 0,
                            # leave as they are in the DIR-File and just change the death_code.
                            # Otherwise, change existing death_time, death_latitude, death_longitude
                            # and death_code in the DIR-File.
                            if (death_time != 0 or death_latitude != 0 or death_longitude != 0):
                                if (int(death_time) > 0):
                                    # The 8th column in DIR-File represents the death time.
                                    # The 9th column in DIR-File represents the death latitude.
                                    # The 10th column in DIR-File represents the death longitude.
                                    row[7]  = death_time
                                    row[8]  = death_latitude
                                    row[9]  = death_longitude

                            # The 22th column in DIR-File represents the death code.
                            row[21] = death_code

                            # Did any change occur?
                            if (old_row[7] != row[7] or     # death_time
                                old_row[8] != row[8] or     # death_latitude
                                old_row[9] != row[9] or     # death_longitude
                                old_row[21] != row[21]):    # death_code
                                error_message = common.validate_dirfl_record(row)
                                if (error_message == None):
                                    # Replace with new values.
                                    new_directory_file[idx] = row

                                    # Prints out a log of the buoy's parameters before any changes are applied.
                                    message = '{:>19}'.format(str(int(row[0])))                 # buoy_id
                                    message = message + '{:>13}'.format(f"{old_row[7]:.3f}")    # death_time
                                    message = message + '{:>9}'.format(f"{old_row[8]:.3f}")     # death_latitude
                                    message = message + '{:>9}'.format(f"{old_row[9]:.3f}")     # death_longitude
                                    message = message + '{:>9}'.format(int(old_row[21]))        # death_code
                                    print(message)
                                    # Logs the modified data to the console.
                                    message = '{:>32}'.format(f"{row[7]:.3f}")                  # death_time
                                    message = message + '{:>9}'.format(f"{row[8]:.3f}")         # death_latitude
                                    message = message + '{:>9}'.format(f"{row[9]:.3f}")         # death_longitude
                                    message = message + '{:>9}'.format(int(row[21]))            # death_code
                                    print(message)
                                    print(' ')
                                else:
                                    print("Error: Check " + f"{int(row[0])}" + " " + error_message)
                        else:
                            print(str(buoy_id) + ": no match found in DIR-File.")
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

# This function is used to change the status of a buoy to dead in DIR-File,
# while creating a timestamped backup copy beforehand.
# It reads info from a previously created file with format:
#     buoy_id, death_time, death_latitude, death_longitude, death_code.

# If date_time, dead_latitude and dead_longitude are:
#   = 0, leave as they are in the DIR-File and just change the dead_code.
#   > 0, change existing date_time, dead_latitude, dead_longitude and dead_code in the DIR-File.
def update_dead_info():
    print('\n')
    print(f"{' ' * 9}{'Enter complete file name where info for records are,'}")
    input_file = str(input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/dead.lis): '}"))

    print('\n')
    print(f"{' ' * 9}{'Expected file format: id, death_time, death_latitude, death_longitude, death_code'}")

    print('\n')
    print(f"{' ' * 9}{'Note:'}")
    print(f"{' ' * 13}{'If death_time, death_latitude and death_longitude are equal 0,'}")
    print(f"{' ' * 13}{'leave as they are in the DIR-File and just change the death_code.'}")
    print(f"{' ' * 13}{'Otherwise, change existing death_time, death_latitude, death_longitude and death_code in the DIR-File.'}")
    
    new_directory_file = update_dead_info_in_directory_file(input_file)

    if (new_directory_file != None):
        # Update the directory file
        dirfl = DirectoryFile()
        dirfl.wdirfl50(new_directory_file)
    else:
        print(f"{' ' * 4}" + "No changes")

