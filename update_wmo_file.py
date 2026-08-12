#!/usr/bin/python

# Programer: CG August 2026

from file_manager import FileManager
from common import CommonFunctions
from database_manager import DatabaseManager

def update_wmo_in_directory_file(input_file):
#    print(*input_file, sep ='\n')
    result = None
    
    # Loads the directory file
    db_manager = DatabaseManager()
    directory_file = db_manager.select_all_dirfl()
    # Makes a copy of DIR-File.
    new_directory_file = directory_file.copy()

    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n')
    print("Number of DIR-File records: ", len(directory_file), '\n')

    print("Wait!: Changing WMO numbers in directory file..." + '\n')

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
                        wmo     = float(columns[1])

                        dirfl_wmo_column = 1 # (0-indexed)
                        if (common.value_exits_2D(wmo, dirfl_wmo_column, directory_file) == False):                        
                            # Looks for the ID in the DIR-File.
                            idx = db_manager.select_row_number_dirfl(buoy_id)
                            if (idx >= 0 ):
                                # Buoy ID was found in DIR-File
                                # Makes copies of DIR-File's row.
                                old_row = directory_file[idx].copy()
                                row = old_row.copy()

                                # The 2nd column in DIR-File represents the WMO number.
                                row[1] = wmo
                                # The WMO number was changed?
                                if (old_row[1] != row[1]):
                                    # Replace with new values.
                                    new_directory_file[idx] = row

                                    # Prints out a log of the buoy's parameters before any changes are applied.
                                    print(f"{' ' * 4}" + f"{int(row[0])}")
                                    print(f"{' ' * 6}" + "Old: WMO = " + f"{old_row[1]}")
                                    # Logs the modified data to the console.
                                    print(f"{' ' * 6}" + "New: WMO = " + f"{row[1]}")
                                    print(' ')
                            else:
                                print(buoy_id + ": no match found in DIR-File.")
                        else:
                            print("Error: WMO number " + f"{int(wmo)}" + " already exists.")
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
            file.close() # Always executes, ensuring the stream is freed

    if (common.compare_2D_float_lists(new_directory_file, directory_file) == False):
        result = new_directory_file

    return result

# This function is used to add WMO numbers in the directory file (DIR_File),
# while creating a timestamped backup copy beforehand.
# It reads info from a previously created file with format: buoy id, wmo.
def update_wmo():
    print('\n')
    print(f"{' ' * 9}{'Enter complete file name where info for records are,'}")
    input_file = input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/wmo.lis): '}")

    print('\n')
    print(f"{' ' * 9}{'Expected file format: id, wmo'}")

    new_directory_file = update_wmo_in_directory_file(input_file)

    if (new_directory_file != None):
        # Update the directory file
        db_manager = DatabaseManager()
        db_manager.update_all_dirfl(new_directory_file)
    else:
        print(f"{' ' * 4}" + "No changes")
