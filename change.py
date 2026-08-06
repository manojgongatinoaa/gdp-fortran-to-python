#!/usr/bin/python

# Programer: CG August 2026

from common import CommonFunctions
from directory_file import DirectoryFile
from verify import verify

# This function changes a record at a time in the DIR-File.
# Parameter:
#   jd_to_date     - Flag controlling date formatting. If True, timestamps convert 
#                    to Month/Day/Year. If False, they print as raw decimals.
#   change_record  - Flag to distinguish whether the record needs to be changed or is 
#                    merely being displayed.
def change(jd_to_date, change_record):
    # Loads the directory file
    dirfl = DirectoryFile()
    directory_file = dirfl.rdirfl50()

    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n')
    print("Number of DIR-File records: ", len(directory_file), '\n')

    print('\n')
    buoy_id = input(f"{' ' * 9}{'Enter buoy ID to work with: '}")

    # Looks for the ID in the DIR-File.
    common = CommonFunctions()
    idx = common.get_id_position_in_dirfl(int(buoy_id), directory_file)
    if (idx >= 0 ):
        # Buoy ID was found in DIR-File
        old_row = directory_file[idx].copy()
        new_row = verify(old_row, jd_to_date, change_record)
        if (old_row != new_row):
            error_message = common.validate_dirfl_record(new_row)
            if (error_message == None):  # Record is valid
                # Prints out a log of the buoy's parameters before any changes are applied.
                print('\n')
                old = ", ".join(str(num) for num in old_row)
                print(f"{' ' * 6}" + "Old: " + old)
                # Logs the modified data to the console.
                new = ", ".join(str(num) for num in new_row)
                print(f"{' ' * 6}" + "New: " + new)
                print(' ')

                # Replace with the new values.
                directory_file[idx] = new_row

                # Update the DIR-File.
                dirfl = DirectoryFile()
                dirfl.wdirfl50(directory_file)
            else:
                print('\n')
                print(" " + f"{int(new_row[0])}" + " " + error_message)
        else:
            print('\n')
            print(f"{' ' * 6}{'No changes'}")
    else:
        print('\n')
        print(buoy_id + ": no match found in DIR-File.")
