#!/usr/bin/python

# programer: CG July 2026

import shutil
import math

from file_manager import FileManager
from constants import BACKUP_DIR

# Class containing the most commonly used functions
class CommonFunctions:
    # **** Validation ***
    def is_float(self, element):
        try:
            float(element)
            return True
        except ValueError:
            return False

    def value_exits_2D(self, target_value, column, matrix) -> bool:
        col_index = column  # Checking the X column (0-indexed)

        # Check if target exists in that column
        return any(row[col_index] == target_value for row in matrix)
            
    def validate_dirfl_record(self, record):
        result = None
        
        start_time = record[4]          # The 5th column in DIR-File represents the deployment date.
        end_time = record[7]            # The 8th column in DIR-File represents the date of last fix.
        drogue_off_date = record[14]    # The 15th column in DIR-File represents the drogue-off date.

        # Make sure the drogue-off date is not after end_time in DIR-File.
        if (end_time > 0.0 and drogue_off_date > end_time):
            result = "drogue-off date is after end_time in DIR-File."
        # Make sure the drogue-off date is not before start_time in DIR-File.
        elif (drogue_off_date > 1.0 and drogue_off_date < start_time):
            result = "drogue-off date is before start_time in DIR-File."
        else:
            # Make sure the start_time is not after end_time in DIR-File.
            if (end_time > 0.0 and start_time > end_time):
                result = "start_time is after end_time in DIR-File."
                                
        return result
    
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

    # *** Common called methods ***

    # To change an element in a specific column of a tmpfl30.dat file.
    def change_element_tmpfl(self, file_path, idx_row, idx_column, new_value):
        lines = []
        try:
            # Step 1: Read all lines into memory
            with open(file_path, 'r') as file:
                lines = file.readlines()
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if file:
                file.close # Always executes, ensuring the stream is freed

        if (len(lines) > 0):
            # Split the line
            columns = lines[idx_row].split()

            # Creates old line to add existing in the tmpfl30.dat file.
            old_line = '{:>16}'.format(columns[0])              # buoy ID
            old_line = old_line + '{:>8}'.format(columns[1])    # esperiment number
            old_line = old_line + '{:>12}'.format(columns[2])   # start time
            old_line = old_line + '{:>12}'.format(columns[3])   # end time
            old_line = old_line + '\n'
        
            # Step 2: Modify the element at Row idx_row, Column idex_column
            columns[idx_column] = new_value

            # Creates new line to add to the tmpfl30.dat file.
            new_line = '{:>16}'.format(columns[0])              # buoy ID
            new_line = new_line + '{:>8}'.format(columns[1])    # esperiment number
            new_line = new_line + '{:>12}'.format(columns[2])   # start time
            new_line = new_line + '{:>12}'.format(columns[3])   # end time
            new_line = new_line + '\n'
            
            # Reconstruct the line and save it back to the list
            lines[idx_row] = new_line

            # Validate: start time must be less than end time if end time greater than 0.0
            start_time = float(columns[2])
            end_time = float(columns[3])

            valid = False
            if (end_time == 0.0):
                valid = True
            elif (end_time > 0.0 and (start_time <= end_time)):
                valid = True
            if (valid == True):
                file = None
                try:
                    # Step 3: Write the lines back to the file
                    with open(file_path, 'w') as file:
                        file.writelines(lines)
                    print('\n' + f"{' ' * 9}{'Old: '}{old_line}")
                    print(f"{' ' * 9}{'New: '}{new_line}")
                except OSError as e:
                    # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
                    # f"Message: {e.strerror}")     = Human-readable OS error string
                    # f"Target File: {e.filename}") = Name of the file causing the issue
                    message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
                    print(message)
                finally:
                    if file:
                        file.close # Always executes, ensuring the stream is freed
            else:
                print('\n')
                print(f"{'Error: Start time must be less than end time ('}{new_line}{')'}")


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

    # This function, given an ID, returns the position of that buoy in the tmpfl30.dat filr.
    # Parameters:
    #     buoy_id: An integer used to locate its position in the directory file.
    #     tmpfl30: A list with all records in tmpfl30.dat file.
    # Return:
    #    pos: Row index position corresponding to the buoy ID in tmpfl30.dat file.
    def get_id_position_in_tmpfl30(self, buoy_id, tmpfl30) -> int:
        pos = 0
        found = False

        # Looks for the ID in the tmpfl30.dat.
        for row in tmpfl30:
            # row example: 
            # 300534068922080.   2222.   17214.625       0.000

            # The 1st column in tmpfl30.dat represents the buoy ID. 
            if (buoy_id in row):
                found = True
                break
            pos += 1

        if (not found):
            pos = -1

        return pos
