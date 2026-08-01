#!/usr/bin/python

# Programer: CG August 2026

from directory_file import DirectoryFile
from file_manager import FileManager
from common import CommonFunctions

def update_start_info_in_directory_file(input_file):
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

    print("Wait!: Changing start time and start position in directory file..." + '\n')

    file = None
    file_manager = FileManager()
    input_file_path = file_manager._resolve_path(input_file)
    common = CommonFunctions()
    try:
        # input_file format: buoy id, start time, start latitude, start longitude.
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
                    if (len(columns) > 3):
                        buoy_id         = int(columns[0])
                        start_time      = float(columns[1])
                        start_latitude  = float(columns[2])
                        start_longitude = float(columns[3])
                        
                        # Looks for the ID in the DIR-File.
                        idx = common.get_id_position_in_dirfl(buoy_id, directory_file)
                        if (idx >= 0 ):
                            # Buoy ID was found in DIR-File
                            # Makes copies of DIR-File's row.
                            old_row = directory_file[idx].copy()
                            row = old_row.copy()
                            
                            # The 5th column in DIR-File represents the death time.
                            # The 6th column in DIR-File represents the death latitude.
                            # The 7th column in DIR-File represents the death longitude.
                            row[4]  = start_time
                            row[5]  = start_latitude
                            row[6]  = start_longitude
                            
                            # Did any change occur?
                            if (old_row[4] != row[4] or     # start_time
                                old_row[5] != row[5] or     # start_latitude
                                old_row[6] != row[r]):       # start_longitude
                                # Replace with new values.
                                new_directory_file[idx] = row

                                # Prints out a log of the buoy's parameters before any changes are applied.
                                message = '{:>19}'.format(str(int(row[0])))                 # buoy_id
                                message = message + '{:>13}'.format(f"{old_row[4]:.3f}")    # death_time
                                message = message + '{:>9}'.format(f"{old_row[5]:.3f}")     # death_latitude
                                message = message + '{:>9}'.format(f"{old_row[6]:.3f}")     # death_longitude
                                print(message)
                                # Logs the modified data to the console.
                                message = '{:>32}'.format(f"{row[4]:.3f}")                  # death_time
                                message = message + '{:>9}'.format(f"{row[5]:.3f}")         # death_latitude
                                message = message + '{:>9}'.format(f"{row[6]:.3f}")         # death_longitude
                                print(message)
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

# This routine is used to change the start time, lat, lon of an existing record in DIR-File,
# while creating a timestamped backup copy beforehand.
# It reads info from a previously created file with format:
#     buoy_id, start_time, start_latitude, start_longitude (-long is East, +long 0-180 = W)
def update_start_info():
    print('\n')
    print(f"{' ' * 9}{'Enter complete file name where info for records are,'}")
    input_file = str(input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/start.lis): '}"))

    print('\n')
    print(f"{' ' * 9}{'Expected file format: id, start_time, start_latitude, start_longitude (-long is East, +long 0-180 = W)'}")

    new_directory_file = update_start_info_in_directory_file(input_file)

    if (new_directory_file != None):
        # Update the directory file
        dirfl = DirectoryFile()
        dirfl.wdirfl50(new_directory_file)
    else:
        print(f"{' ' * 4}" + "No changes")
