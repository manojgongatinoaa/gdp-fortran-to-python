#!/usr/bin/python

# programer: CG August 2026

# Import Module
import struct

from constants import WCK_DIR
from constants import data_type_columns
from common import CommonFunctions

# Chunk size:
# Because each row has 4 columns and each number is a 32-bits float (4 bytes), 
# each line in the file is exactly 16 bytes long.
COLUMNS = data_type_columns["p_file"]
CHUNK_SIZE = COLUMNS*4
# Format string:
# 4f = 4 floats (16 bytes)
FORMAT_STRING = f"{'<'}{COLUMNS}{'f'}"

# Class to safely and easily manage common P-File operations.
class PFile:
    def __init__(self, buoy_id: str):
        self.path = f"{WCK_DIR}{'p'}{buoy_id}{'.dat'}"
        self.pfl = []
        self.start_time = None
        self.end_time = None

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    # Read P-File: This is acting as the data loader.
    #              It opens the binary P-File, reading the data row-by-row
    #              and stops automatically when it hits the end of valid data.
    #              P-File is raw binary (not human-readable text).
    #
    # Return:
    #     pfl - The P-File
    def rpfl(self):
        p_file = None
        try:
            # Opens the file for reading binary data.
            with open(self.path, 'rb') as p_file:
                while True:
                    # For large binary files, reading the entire file at once may consume a lot of memory.
                    # In such cases, it is better to read the file in smaller chunks using read(size).
                    # The file is read in blocks of 16 bytes until no more data is available.
                    chunk = p_file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    # row format: time, lat, lon, q.i  
                    # row example: 
                    # 16545.37890625 39.610599517822266 11.184599876403809 9.09000015258789
                    tuple = struct.unpack(FORMAT_STRING, chunk)
                    # Convert to list because Python tuples are immutable
                    self.pfl.append(list(tuple))
                        
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if p_file:
                p_file.close() # Always executes, ensuring the stream is freed

        length = len(self.pfl)
        if length > 1:
            # The first record is a header indicating how many rows were entered
            # (Fortran legacy).
            row = self.pfl[1] # second record.
            self.start_time = row[0]
            row = self.pfl[length - 1] # jump to the final record.
            self.end_time = row[0]

        # A 2D array.
        # It holds the P-File for an specific buoy.
        return self.pfl
        
    # This function write drifter data into the binary (unformatted) direct-access
    # file called p<BUOY_ID>.dat, while creating a timestamped backup copy beforehand.
    def wpfl(self, p_file):
        common = CommonFunctions()
        # Automatically create a timestamped backup copy of the existing P-File.
        backup_file = common.create_timestamped_backup(self.path)
        if (backup_file):
            print('\n' + "P-File backup created:", backup_file, "with today's date/time.")
        
        file = None
        # Flatten the 2D list into a 1D list
        flat_data = [item for row in p_file for item in row]
        try:
            # Open the file in 'wb' (write binary) mode
            with open(self.path, "wb") as file:
                # 'f' is float32; multiplying by len(flat_data) packs all items
                binary_data = struct.pack(f"<{len(flat_data)}f", *flat_data)
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
