#!/usr/bin/python

# programer: CG July 2026

import constants

# A helper class to run database queries.
# The primary objective is to ensure these functions can be easily
# replaced once the database migration is complete.
class DatabaseManager:
    def select_buoy_manufacturer(self):
        # Extracting the 1st and 4th columns (indices 0 and 3)
        columns_data = []

        try:
            file = None
            # /phodnet/drifter/data/files/tpb_ab_coef15.dat includes manufacturer codes, column 4.
            with open(constants.TPB_AB_COEF15_DAT, "r") as file:
                for line in file:
                    # split() without arguments automatically handles any consecutive whitespace
                    parts = line.strip().split()
                    
                    # Ensure the line has enough data to avoid IndexError
                    if len(parts) > 3:
                        # Removes '.' at the end
                        columns_data.append((parts[0][:-1], parts[3][:-1]))
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if file:
                file.close # Always executes, ensuring the stream is freed

        # Discard the first element, which is the header.
        if (len(columns_data) > 0):
            columns_data.pop(0)
        #print(*columns_data, sep="\n")

        return columns_data
    
    def select_wmo(self, buoy_id):
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
                file.close # Always executes, ensuring the stream is freed

        wmo = 0
 
        for i in range(len(matrix)):
            # Checks if the target ID equals the stored ID.
            if matrix[i][0] == buoy_id:
                # If a match is found extract the WMO
                wmo = matrix[i][1]
                break

        return wmo
