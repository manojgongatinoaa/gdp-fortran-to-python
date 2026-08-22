#!/usr/bin/python

# programer: CG July 2026

import shutil
import math
from datetime import date
from datetime import datetime
from datetime import timedelta

from file_manager import FileManager
from database_manager import DatabaseManager
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

    def is_valid_date(self, date_string, date_format="%Y-%m-%d"):
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    def value_exits_2D(self, target_value, column, matrix) -> bool:
        col_index = column  # Checking the X column (0-indexed)

        # Check if target exists in that column
        return any(row[col_index] == target_value for row in matrix)
            
    def validate_dirfl_record(self, record):
        result = None

        buoy_id         = record[0]     # The 1st column in DIR-File represents the buoy ID.
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

    # Find duplicate records in a large 2D array based on the column's index.
    # Output: [[22, '300534060014780', ...], [29376, '300534060014780', ...], ...]
    def find_duplicate_rows_by_col(self, matrix, column):
        from collections import defaultdict
        # Group row data and row numbers by the first column value
        groups = defaultdict(list)
        for idx, row in enumerate(matrix):
            groups[row[column]].append((idx, row))
        
        # Extract groups that appear more than once
        duplicated_rows = []
        for key, items in groups.items():
            if len(items) > 1:
                for idx, row in items:
                    # Add row number to the front of the row
                    duplicated_rows.append([idx] + list(row))
                
        return duplicated_rows
    
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

    # Format into a "MM DD.DD YYYY" string format
    def format_date(self, date):
        result = ''

        mm = '{:>2}'.format(f"{date[1]}")
        dd = '{:>5}'.format(f"{date[2]:.2f}")
        result = f"{mm} {dd} {date[0]}"

        return result

    def jd_to_date(self, jd):
        r = self.jd_to_date_base(jd)
        return date(r[0], r[1], int(r[2]))

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
                base_date = date(year, month, day_int)
                
                # Add fractional part as a fraction of a day (24 hours)
                total_time = base_date + timedelta(days = day_frac)
                result =  True
        except ValueError:
            result = False
        return result

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
    

