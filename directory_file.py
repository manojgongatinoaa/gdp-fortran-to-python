#!/usr/bin/python

# programer: CG July 2026

# Import Module
import struct

from constants import DIR_FILE
from constants import data_type_columns
from common import CommonFunctions

# Chunk size:
# Because each row has 22 columns and each number is a 64-bits double (8 bytes), 
# each line in the file is exactly 176 bytes long.
COLUMNS = data_type_columns["d_file"]
CHUNK_SIZE = COLUMNS*8
# Format string:
# 22d = 22 doubles (176 bytes)
FORMAT_STRING = f"{'<'}{COLUMNS}{'d'}"

# Class to safely and easily manage common DIR-File operations.
class DirectoryFile:

    def __init__(self):
        self.path = DIR_FILE

    # Read DIR-File: This is acting as the data loader.
    #                It opens the binary DIR-File, reading the data row-by-row
    #                and stops automatically when it hits the end of valid data.
    #                DIR-File is raw binary (not human-readable text).
    #
    # Return:
    # dirfl - The DIR-File
    def rdirfl50(self):
        dirfl = []

        directory_file = None
        try:
            # Opens the file for reading binary data.
            with open(self.path, 'rb') as directory_file:
                while True:
                    # For large binary files, reading the entire file at once may consume a lot of memory.
                    # In such cases, it is better to read the file in smaller chunks using read(size).
                    # The file is read in blocks of 176 bytes until no more data is available.
                    chunk = directory_file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    buoy_id = struct.unpack('d', chunk[:8])[0] # First column

                    # If the buoy_id is less than or equal to 0, it means
                    # it has reached a blank/sentinel row marking the end
                    # of real data.
                    if buoy_id > 0:
                        # row example: 
                        # 300534064897810.0, 4401656.0, 2222.0, 48.0, 17201.041015625,
                        # 43.189998626708984, -28.010000228881836, 17261.75, 41.73809814453125, -27.218000411987305,
                        # 41.0, 44.0, -29.0, -27.0, 17201.041015625,
                        # 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0
                        tuple = struct.unpack(FORMAT_STRING, chunk)
                        # Convert to list because Python tuples are immutable
                        dirfl.append(list(tuple))
                        
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if directory_file:
                directory_file.close() # Always executes, ensuring the stream is freed

        # A 2D array.
        # It holds the directory file buoys across 22 parameters.
        return dirfl
        
    # This function write drifter data into the binary (unformatted) direct-access file called dirfl50.dat,
    # while creating a timestamped backup copy beforehand.
    def wdirfl50(self, directory_file):
        common = CommonFunctions()
        # Automatically create a timestamped backup copy of the existing DIR-File.
        backup_file = common.create_timestamped_backup(DIR_FILE)
        if (backup_file):
            print('\n' + "DIR-File backup created:", backup_file, "with today's date/time.")
        
        file = None
        # Flatten the 2D list into a 1D list
        flat_data = [item for row in directory_file for item in row]
        try:
            # Open the file in 'wb' (write binary) mode
            with open(DIR_FILE, "wb") as file:
                # 'd' is float64; multiplying by len(flat_data) packs all items
                binary_data = struct.pack(f"<{len(flat_data)}d", *flat_data)
                file.write(binary_data) 

        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if file:
                file.close() # Always executes, ensuring the stream is freed
