#!/usr/bin/python

# programer: CG August 2026

# Import Module
import struct

from constants import RAW_DIR
from constants import data_type_columns
from common import CommonFunctions

# Chunk size:
# Because each row has 11 columns and each number is a 32-bits float (4 bytes), 
# each line in the file is exactly 44 bytes long.
COLUMNS = data_type_columns["b_file"]
CHUNK_SIZE = COLUMNS*4
# Format string:
# 11f = 11 floats (44 bytes)
FORMAT_STRING = f"{'<'}{COLUMNS}{'f'}"

# Class to safely and easily manage common B-File operations.
class BFile:
    def __init__(self, buoy_id: str):
        self.path = f"{RAW_DIR}{'b'}{buoy_id}{'.dat'}"
        self.bfl = []
        self.start_time = None
        self.end_time = None

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    # Read B-File: This is acting as the data loader.
    #              It opens the binary B-File, reading the data row-by-row
    #              and stops automatically when it hits the end of valid data.
    #              B-File is raw binary (not human-readable text).
    #
    # Return:
    #     bfl - The B-File
    def rbfl(self):
        b_file = None
        try:
            # Opens the file for reading binary data.
            with open(self.path, 'rb') as b_file:
                while True:
                    # For large binary files, reading the entire file at once may consume a lot of memory.
                    # In such cases, it is better to read the file in smaller chunks using read(size).
                    # The file is read in blocks of 44 bytes until no more data is available.
                    chunk = b_file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    # row format: time, lat, lon, s.time, sws, tmp, volt, t2, t3, t4, q.i
                    # row example: 
                    # 16766.541015625 62.20600128173828 341.8599853515625 16766.541015625
                    # 32.0 9.050018310546875 11.0 1005.2999877929688 0.0 0.0 9.0600004196167
                    tuple = struct.unpack(FORMAT_STRING, chunk)
                    # Convert to list because Python tuples are immutable
                    self.bfl.append(list(tuple))
                        
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if b_file:
                b_file.close() # Always executes, ensuring the stream is freed

        length = len(self.bfl)
        if length > 1:
            # The first record is a header indicating how many rows were entered
            # (Fortran legacy).
            row = self.bfl[1] # second record.
            self.start_time = row[0]
            row = self.bfl[length - 1] # jump to the final record.
            self.end_time = row[0]

        # A 2D array.
        # It holds the B-File for an specific buoy.
        return self.bfl
        
    # This function write drifter data into the binary (unformatted) direct-access
    # file called b<BUOY_ID>.dat, while creating a timestamped backup copy beforehand.
    def wbfl(self, b_file):
        common = CommonFunctions()
        # Automatically create a timestamped backup copy of the existing B-File.
        backup_file = common.create_timestamped_backup(self.path)
        if (backup_file):
            print('\n' + "B-File backup created:", backup_file, "with today's date/time.")
        
        file = None
        # Flatten the 2D list into a 1D list
        flat_data = [item for row in b_file for item in row]
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
