#!/usr/bin/python

# programer: CG July 2026

import shutil
import math

from file_manager import FileManager
from constants import BACKUP_DIR

# Class containing the most commonly used functions
class CommonFunctions:
    def create_timestamped_backup(self, path):
        timestamped_backup_file = ''
        try:
            file_manager = FileManager()
            timestamped_backup_file = file_manager.create_timestamped_backup(path, BACKUP_DIR)
 
        except shutil.SameFileError:
            # Raised if source and destination are exactly the same file
            print("Error: Source and destination represent the same file.")

        except PermissionError:
            # Raised if you lack read permissions for source or write permissions for destination
            print("Error: Permission denied. Check file or folder access rights.")

        except FileNotFoundError:
            # Raised if the source file or the destination directory path does not exist
            print("Error: The source file or target directory was not found.")

        except IsADirectoryError:
            # More common with shutil.copyfile() if destination is an existing directory instead of a file path
            print("Error: The destination is a directory, not a file layout.")

        except OSError as e:
            # Catch-all for any other system-level errors (disk full, network drop, etc.)
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)

        return timestamped_backup_file

    # This function, given an ID, returns the position of that buoy in the directory file.
    # Parameters:
    #     buoy_id: An integer used to locate its position in the directory file.
    #     directory_file: A list with all records in directory file.
    # Return:
    #    pos: Row index position corresponding to the buoy ID in DIR-File.
    def get_id_position_in_dirfl(self, buoy_id, directory_file):
        pos = 0
        found = False

        # Looks for the ID in the DIR-File.
        for row in directory_file:
            # row example: 
            # 300534064897810.0, 4401656.0, 2222.0, 48.0, 17201.041015625,
            # 43.189998626708984, -28.010000228881836, 17261.75, 41.73809814453125, -27.218000411987305,
            # 41.0, 44.0, -29.0, -27.0, 17201.041015625,
            # 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0

            # The 1st column in DIR-File represents the buoy ID. 
            if (buoy_id == int(row[0])):
                found = True
                break
            pos += 1

        if (not found):
            pos = -1

        return pos
    
    # This function compares two 2D float arrays
    # Pramater:
    #    list1 - 2D float array
    #    list2 - 2D float array
    # Return:
    #    True -  if both arrays are equal
    #    False - if the arrays are different
    # Note:
    #    Because floating-point numbers have precision limitations, 
    #    using standard operators like == can cause unexpected False. 
    def compare_2D_float_lists(self, list1, list2):
        # Complete match check
        all_match = all(
            math.isclose(a, b) 
            for row1, row2 in zip(list1, list2) 
            for a, b in zip(row1, row2)
        )
        return all_match
