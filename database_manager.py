#!/usr/bin/python

# programer: CG July 2026

import constants

from tmpfl_file import TmpflFile
from file_manager import FileManager

# A helper class to run database queries.
# The primary objective is to ensure these functions can be easily
# replaced once the database migration is complete.
class DatabaseManager:
    #******************************
    #*** tpb_ab_coef15.dat file ***
    #******************************
    def select_all_manufacturer(self) -> list[str]:
        # Extracting the 1st and 4th columns (indices 0 and 3)
        matrix = []
        try:
            file = None
            # /phodnet/drifter/data/files/tpb_ab_coef15.dat includes
            # manufacturer codes = column 4.
            with open(constants.TPB_AB_COEF15_DAT, "r") as file:
                for line in file:
                    # split() without arguments automatically handles any consecutive whitespace
                    columns = line.strip().split()
                    
                    # Ensure the line has enough data to avoid IndexError
                    if len(columns) > 3:
                        # Removes '.' at the end
                        matrix.append((columns[0][:-1], columns[3][:-1]))
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if file:
                file.close() # Always executes, ensuring the stream is freed

        # Discard the first element, which is the header.
        if (len(matrix) > 0):
            matrix.pop(0)
        #print(*columns_data, sep="\n")
        return matrix

    def select_manufacturer(self, buoy_id):
        manufacturer = None
        matrix = self.select_all_manufacturer()
        for i in range(len(matrix)):
            # Checks if the target ID equals the stored ID.
            if matrix[i][0] == buoy_id:
                # If a match is found extract the manufacturer
                manufacturer = matrix[i][1]
                break
        return manufacturer

    #*************************
    #*** IMEI_LUT.dat file ***
    #*************************

    def select_all_wmo(self) -> list[str]:
        matrix = []
        try:
            file = None
            # IMEI_LUT.dat is a more comprehensive source, which compiles WMO's
            # from IMEI_LUT_DAT.dat, ghrsst buoys, SIO files, etc. 
            with open(constants.IMEI_LUT_DAT, "r") as file:
                for line in file:
                    # split() without arguments automatically handles any consecutive whitespace
                    parts = line.strip().split()
                    
                    # Ensure the line has enough data to avoid IndexError
                    if len(parts) > 1:
                        # Extracting the 1st and 3rd columns (indices 0 and 2)
                        matrix.append((parts[0], parts[2]))
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if file:
                file.close() # Always executes, ensuring the stream is freed
        return matrix

    def select_wmo(self, buoy_id):
        matrix = self.select_all_wmo()
        wmo = 0
        for i in range(len(matrix)):
            # Checks if the target ID equals the stored ID.
            if matrix[i][0] == buoy_id:
                # If a match is found extract the WMO
                wmo = matrix[i][1]
                break
        return wmo

    # This function, given an ID, returns the row number in the IMEI_LUT.dat file.
    # Parameters:
    #     buoy_id: An integer used to locate its position in the IMEI_LUT.dat file.
    # Return:
    #    row_number: Row index corresponding to the buoy ID in IMEI_LUT.dat.
    def select_row_number_wmofl(self, buoy_id: int) -> int:
        wmos = self.select_all_wmo()

        row_number = 0

        # Looks for the ID in the DIR-File.
        for row in wmos:
            # row example: 
            # 300534064897810.0, 4401656.0, 2222.0, 48.0, 17201.041015625,
            # 43.189998626708984, -28.010000228881836, 17261.75, 41.73809814453125, -27.218000411987305,
            # 41.0, 44.0, -29.0, -27.0, 17201.041015625,
            # 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0

            # The 2nd column in DIR-File represents the WMO number.
            if (buoy_id == int(row[0])):
                # Found
                break
            row_number += 1

        if (row_number == len(wmos)):
            row_number = -1

        return row_number

    #************************
    #*** tmpfl30.dat file ***
    #************************
    
    def select_all_tmpfl30(self) -> list[str]:
        tmpfl_file = TmpflFile()
        fl_manager = FileManager()
        file_path = fl_manager._resolve_path(tmpfl_file.path)

        rows = []
        try:
            with open(file_path, 'r') as file:
                rows = file.readlines()
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if file:
                file.close() # Always executes, ensuring the stream is freed

        return rows

    def update_all_tmpfl30(self, lines):
        tmpfl_file = TmpflFile()
        fl_manager = FileManager()
        file_path = fl_manager._resolve_path(tmpfl_file.path)

        file = None
        try:
            # Write the lines back to the file
            with open(file_path, 'w') as file:
                file.writelines(lines)
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if file:
                file.close() # Always executes, ensuring the stream is freed

    # To change an element in a specific column of a tmpfl30.dat file.
    def change_element_tmpfl(self, idx_row, idx_column, new_value):
        db_manager = DatabaseManager()
        rows = db_manager.select_all_tmpfl30()
    
        if (len(rows) > idx_row + 1):
            row = rows[idx_row] # an string
            columns = row.split() # a list
            if (len(columns) > 3):
                # Creates old line to print a report.
                old_row = '{:>16}'.format(columns[0])             # buoy ID
                old_row = old_row + '{:>8}'.format(columns[1])    # esperiment number
                old_row = old_row + '{:>12}'.format(columns[2])   # start time
                old_row = old_row + '{:>12}'.format(columns[3])   # end time
                old_row = old_row + '\n'
            
                # Modify the element at Row idx_row, Column idx_column
                columns[idx_column] = new_value

                # Validate:
                #     start time must be less than end time if end time greater than 0.0
                start_time = float(columns[2])
                end_time = float(columns[3])

                valid = False
                if (end_time == 0.0):
                    valid = True
                elif (end_time > 0.0 and (start_time <= end_time)):
                    valid = True
                if (valid):
                    # Creates new line.
                    new_row = '{:>16}'.format(columns[0])             # buoy ID
                    new_row = new_row + '{:>8}'.format(columns[1])    # esperiment number
                    new_row = new_row + '{:>12}'.format(columns[2])   # start time
                    new_row = new_row + '{:>12}'.format(columns[3])   # end time
                    new_row = new_row + '\n'
                    
                    # Reconstruct the line to save it back to the tmpfl30.dat file.
                    rows[idx_row] = new_row

                    print('\n' + f"{' ' * 9}{'Old: '}{old_row}")
                    print(f"{' ' * 9}{'New: '}{new_row}")

                    db_manager.update_all_tmpfl30(rows)

                else:
                    print('\n')
                    print(f"{'Error: Start time must be less than end time ('}{new_row}{')'}")

    # This function, given an ID, returns the row number in the tmpfl30.dat file.
    # Parameters:
    #     buoy_id: A string used to locate its position in the tmpfl30.dat file.
    # Return:
    #    row_number: Row index position corresponding to the buoy ID in tmpfl30.dat file.
    def select_row_number_tmpfl30(self, buoy_id: str) -> int:
        # Read existing tmpfl30.dat file
        tmpfl_file = TmpflFile()
        tmpfl30 = tmpfl_file.rtmpfl30()

        row_number = 0
        found = False

        # Looks for the ID in the tmpfl30.dat.
        for row in tmpfl30:
            # row example: 
            # 300534068922080.   2222.   17214.625       0.000

            # The 1st column in tmpfl30.dat represents the buoy ID. 
            if (buoy_id in row):
                found = True
                break
            row_number += 1

        if (not found):
            row_number = -1

        return row_number

    # This function, given an ID, returns the whole row in the tmpfl30.dat file.
    # Parameters:
    #     buoy_id: A string used to locate its position in the tmpfl30.dat file.
    # Return:
    #    row: Row corresponding to the buoy ID in tmpfl30.dat file.
    def select_row_tmpfl30(self, buoy_id: str) -> str:
        # Read existing tmpfl30.dat file
        tmpfl_file = TmpflFile()
        tmpfl30 = tmpfl_file.rtmpfl30()

        line = None

        # Looks for the ID in the tmpfl30.dat.
        for row in tmpfl30:
            # row example: 
            # 300534068922080.   2222.   17214.625       0.000

            # The 1st column in tmpfl30.dat represents the buoy ID. 
            if (buoy_id in row):
                line = row
                break

        return line

    #****************
    #*** DIR-File ***
    #****************

    def select_all_dirfl(self):
        from directory_file import DirectoryFile        
        # Loads the directory file
        dirfl = DirectoryFile()
        return dirfl.rdirfl50()

    def update_all_dirfl(self, directory_file):
        from directory_file import DirectoryFile
        dirfl = DirectoryFile()
        dirfl.wdirfl50(directory_file)        

    # This function, given an ID, returns the row number in the directory file.
    # Parameters:
    #     buoy_id: An integer used to locate its position in the directory file.
    # Return:
    #    row_number: Row index corresponding to the buoy ID in DIR-File.
    def select_row_number_dirfl(self, buoy_id: int) -> int:
        directory_file = self.select_all_dirfl()

        row_number = 0

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
            row_number += 1

        if (row_number == len(directory_file)):
            row_number = -1

        return row_number

    #*************************
    #*** deployed.log file ***
    #*************************
    
    def select_all_deployed_log(self) -> list[str]:
        from deployed_log import DeployedLog
        deployed_log = DeployedLog()
        fl_manager = FileManager()
        file_path = fl_manager._resolve_path(deployed_log.path)

        rows = []
        try:
            with open(file_path, 'r') as file:
                rows = file.readlines()
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if file:
                file.close() # Always executes, ensuring the stream is freed

        return rows

