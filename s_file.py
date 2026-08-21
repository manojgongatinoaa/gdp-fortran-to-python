#!/usr/bin/python

# programer: CG August 2026

# Import Module
import struct

from constants import WCK_DIR
from constants import data_type_columns
from common import CommonFunctions

# Chunk size:
# Because each row has 7 columns and each number is a 32-bits float (4 bytes), 
# each line in the file is exactly 28 bytes long.
COLUMNS = data_type_columns["s_file"]
CHUNK_SIZE = COLUMNS*4
# Format string:
# 7f = 7 floats (28 bytes)
FORMAT_STRING = f"{'<'}{COLUMNS}{'f'}"

# Class to safely and easily manage common S-File operations.
class SFile:
    def __init__(self, buoy_id: str):
        self.path = f"{WCK_DIR}{'s'}{buoy_id}{'.dat'}"
        self.sfl = []
        self.start_time = None
        self.end_time = None

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    # Read S-File: This is acting as the data loader.
    #              It opens the binary S-File, reading the data row-by-row
    #              and stops automatically when it hits the end of valid data.
    #              S-File is raw binary (not human-readable text).
    #
    # Return:
    #     sfl - The S-File
    def rsfl(self):
        s_file = None
        try:
            # Opens the file for reading binary data.
            with open(self.path, 'rb') as s_file:
                while True:
                    # For large binary files, reading the entire file at once may consume a lot of memory.
                    # In such cases, it is better to read the file in smaller chunks using read(size).
                    # The file is read in blocks of 28 bytes until no more data is available.
                    chunk = s_file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    # row format: time, drog, temp, volt, sen. 4, sen. 5, sen. 6
                    # row example: 
                    # 16766.416015625 39.0 9.050018310546875 11.0 1003.0999755859375 0.0 0.0
                    tuple = struct.unpack(FORMAT_STRING, chunk)
                    # Convert to list because Python tuples are immutable
                    self.sfl.append(list(tuple))
                        
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if s_file:
                s_file.close() # Always executes, ensuring the stream is freed

        length = len(self.sfl)
        if length > 1:
            # The first record is a header indicating how many rows were entered
            # (Fortran legacy).
            row = self.sfl[1] # second record.
            self.start_time = row[0]
            row = self.sfl[length - 1] # jump to the final record.
            self.end_time = row[0]

        # A 2D array.
        # It holds the S-File for an specific buoy.
        return self.sfl
        
    # This function write drifter data into the binary (unformatted) direct-access
    # file called s<BUOY_ID>.dat, while creating a timestamped backup copy beforehand.
    def wsfl(self, s_file):
        common = CommonFunctions()
        # Automatically create a timestamped backup copy of the existing S-File.
        backup_file = common.create_timestamped_backup(self.path)
        if (backup_file):
            print('\n' + "S-File backup created:", backup_file, "with today's date/time.")
        
        file = None
        # Flatten the 2D list into a 1D list
        flat_data = [item for row in s_file for item in row]
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
