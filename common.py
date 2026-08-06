#!/usr/bin/python

# programer: CG July 2026

import shutil
import math
import datetime
from datetime import datetime
from datetime import timedelta

from file_manager import FileManager
from constants import BACKUP_DIR

# Class containing the most commonly used functions
class CommonFunctions:
    # **** Validation ***
    def is_integer(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False

    def is_float(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False

    def value_exits_2D(self, target_value, column, matrix) -> bool:
        col_index = column  # Checking the X column (0-indexed)

        # Check if target exists in that column
        return any(row[col_index] == target_value for row in matrix)
            
    def validate_dirfl_record(self, record):
        result = None

        buoy_id         = record[0]     # The 1nd column in DIR-File represents the buoy ID.
        wmo             = record[1]     # The 2nd column in DIR-File represents the WMO number.
        start_time      = record[4]     # The 5th column in DIR-File represents the deployment date.
        start_lat       = record[5]     # The 6th column in DIR-File represents the deployment latitude coordinate.
        start_lon       = record[6]     # The 7th column in DIR-File represents the deployment longitude coordinate.
        end_time        = record[7]     # The 8th column in DIR-File represents the date of last fix.
        drogue_off_date = record[14]    # The 15th column in DIR-File represents the drogue-off date.

        # Get current date and time
        year    = int(datetime.now().strftime("%Y"))
        month   = int(datetime.now().strftime("%m"))
        day     = int(datetime.now().strftime("%d"))
        now = self.date_to_jd(year, month, day)
        
        if (self.is_float(buoy_id) == False):
            result = "Invalid buoy ID. Please enter a whole number."
        elif (self.is_float(wmo) == False):
            result = "Invalid WMO. Please enter a whole number."
        elif (wmo > float(0) and len(str(abs(int(wmo)))) != 7):
            result = "WMO number have to be 7 digits."
        elif (start_time == float(0)):
            result = "start_time is less than or equal to 0.0"
        elif (start_lat == float(0)):
            result = "start_lat is less than or equal to 0.0"
        elif (start_lon == float(0)):
            result = "start_lon is less than or equal to 0.0"
        elif (start_time > float(0) and start_time > now):
            result = " start_time is in the future."
        elif (end_time > float(0) and end_time > now):
            result = "end_time is in the future."
        elif (drogue_off_date > float(0) and drogue_off_date > now):
            result = "drogue_off_date is in the future."
        # Make sure the drogue-off date is not after end_time in DIR-File.
        elif (end_time > float(0) and drogue_off_date > end_time):
            result = "drogue-off date is after end_time in DIR-File."
        # Make sure the drogue-off date is not before start_time in DIR-File.
        elif (drogue_off_date > float(0) and drogue_off_date < start_time):
            result = "drogue-off date is before start_time in DIR-File."
        # Make sure the start_time is not after end_time in DIR-File.
        elif (end_time > float(0) and start_time > end_time):
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
    def jd_to_date_base(self, jd):
        """
        Convert Julian Day to date.
        
        Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
            4th ed., Duffet-Smith and Zwart, 2011.
        
        Parameters
        ----------
        jd : float
            Julian Day
            
        Returns
        -------
        year : int
            Year as integer. Years preceding 1 A.D. should be 0 or negative.
            The year before 1 A.D. is 0, 10 B.C. is year -9.
            
        month : int
            Month as integer, Jan = 1, Feb. = 2, etc.
        
        day : float
            Day, may contain fractional part.
            
        Examples
        --------
        Convert Julian Day 2446113.75 to year, month, and day.
        
        >>> jd_to_date(2446113.75)
        (1985, 2, 17.25)
        
        convert drifter Julian day
        (Julian day since 12/31/78 = 2443874) to Gregorian calendar.
        This is done by adding 2443874 to the drifter julian day
        """
#        jd = jd + 2443874 + 0.5
        jd = jd + 2443874
        F, I = math.modf(jd)
        I = int(I)        
        A = math.trunc((I - 1867216.25)/36524.25)
        
        if I > 2299160:
            B = I + 1 + A - math.trunc(A / 4.)
        else:
            B = I
            
        C = B + 1524        
        D = math.trunc((C - 122.1) / 365.25)        
        E = math.trunc(365.25 * D)        
        G = math.trunc((C - E) / 30.6001)
        
        day = C - E + F - math.trunc(30.6001 * G)
        
        if G < 13.5:
            month = G - 1
        else:
            month = G - 13
            
        if month > 2.5:
            year = D - 4716
        else:
            year = D - 4715

        return [year, month, day]

    def jd_to_date(self, jd):
        r = self.jd_to_date_base(jd)
        return datetime.date(r[0], r[1], int(r[2]))

    def date_to_jd(self, year, month, day):
        """
        Convert a date to Julian Day.
        
        Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
            4th ed., Duffet-Smith and Zwart, 2011.
        
        Parameters
        ----------
        year : int
            Year as integer. Years preceding 1 A.D. should be 0 or negative.
            The year before 1 A.D. is 0, 10 B.C. is year -9.
            
        month : int
            Month as integer, Jan = 1, Feb. = 2, etc.
        
        day : float
            Day, may contain fractional part.
        
        Returns
        -------
        jd : float
            Julian Day
            
        Examples
        --------
        Convert 6 a.m., February 17, 1985 to Julian Day
        
        >>> date_to_jd(1985,2,17.25)
        2446113.75
        
        """
        if month == 1 or month == 2:
            yearp = year - 1
            monthp = month + 12
        else:
            yearp = year
            monthp = month
        
        # this checks where we are in relation to October 15, 1582, the beginning
        # of the Gregorian calendar.
        if ((year < 1582) or
            (year == 1582 and month < 10) or
            (year == 1582 and month == 10 and day < 15)):
            # before start of Gregorian calendar
            B = 0
        else:
            # after start of Gregorian calendar
            A = math.trunc(yearp / 100.)
            B = 2 - A + math.trunc(A / 4.)
            
        if yearp < 0:
            C = math.trunc((365.25 * yearp) - 0.75)
        else:
            C = math.trunc(365.25 * yearp)
            
        D = math.trunc(30.6001 * (monthp + 1))
        
        jd = B + C + D + day + 1720994.5

        '''
        convert to drifter Julian day
        (Julian day since 12/31/78 = 2443874) to Gregorian calendar.
        This is done by subtracting 2443874 to the drifter julian day
        '''
        jd = jd - (2443874 - 0.5)
        
        return jd

    def validate_date_with_float_day(self, year: int, month: int, day_float: float) -> bool:
        result = False
        try:
            if isinstance(day_float, (int, float)) and day_float > 0:
                day_int = int(day_float)
                day_frac = day_float - day_int
                
                # Validate base year, month, and integer day
                base_date = datetime(year, month, day_int)
                
                # Add fractional part as a fraction of a day (24 hours)
                total_time = base_date + timedelta(days = day_frac)
                result =  True
        except ValueError:
            result = False
        return result

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
    def get_id_position_in_dirfl(self, buoy_id, directory_file) -> int:
        pos = 0

        # Looks for the ID in the DIR-File.
        for row in directory_file:
            # row example: 
            # 300534064897810.0, 4401656.0, 2222.0, 48.0, 17201.041015625,
            # 43.189998626708984, -28.010000228881836, 17261.75, 41.73809814453125, -27.218000411987305,
            # 41.0, 44.0, -29.0, -27.0, 17201.041015625,
            # 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0

            # The 1st column in DIR-File represents the buoy ID.
            if (buoy_id == int(row[0])):
                # Found
                break
            pos += 1

        if (pos == len(directory_file)):
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
    
    # Fills the six generic "sensor" flags.   
    def fill_sensor_type_array(self, buoy_type):
        # Sensor-type array to prepare depending the buoy type
        sensor_type = [0.0] * 6 # # Creates [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(3):
            sensor_type[i] = float(i + 1)   # Elements 1, 2, and 3 are configured with 1.0, 2.0, 3.0.
        if (buoy_type == 9.0):              # If the buoy type is 9.0,
            sensor_type[3] = 9.0            # elements 4, 5, and 6 are configured with 9.0.
            sensor_type[4] = 9.0
            sensor_type[5] = 9.0
        elif (buoy_type == 8.0):            # If the buoy type is 8.0,
            sensor_type[3] = 7.0            # elements 4 and 5 are configured with 7.0.
            sensor_type[4] = 7.0
        elif (buoy_type == 11.0):           # If the buoy type is 11.0 (salinity buoy),
            sensor_type[4] = 9.0            # elements 5 and 6 are configured with 9.0.
            sensor_type[5] = 9.0
        elif (buoy_type == 12.0):           # If the buoy type is 12.0 (barometric/wind),
            sensor_type[3] = 7.0            # element 4 is configured with 7.0,
            sensor_type[4] = 1.0            # element 5 is configured with 1.0.
        elif (buoy_type == 13.0):           # If the buoy type is 13.0 (pure wind),
            sensor_type[4] = 1.0            # element 5 is configured with 1.0.

        return sensor_type
    

