#!/usr/bin/python

# programer: CG August 2026

# Import Module
import struct

from constants import SS_DIR
from common import CommonFunctions

# Chunk size:
# Because each row has 10 columns and each number is a 32-bits double (4 bytes), 
# each line in the file is exactly 40 bytes long.
CHUNK_SIZE = 10*4
# Format string:
# 10f = 10 floats (40 bytes)
FORMAT_STRING = '<10f'

# Class to safely and easily manage common P-File operations.
class KFile:

    def __init__(self, buoy_id: str, print_except = True):
        self.path = f"{SS_DIR}{'k'}{str(buoy_id)}{'.dat'}"
        self.kfl = []
        self.start_time = None
        self.end_time = None
        self.print_except = print_except

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    # Read P-File: This is acting as the data loader.
    #              It opens the binary K-File, reading the data row-by-row
    #              and stops automatically when it hits the end of valid data.
    #              K-File is raw binary (not human-readable text).
    #
    # Return:
    #     kfl - The K-File
    def rkfl(self):
        k_file = None
        try:
            # Opens the file for reading binary data.
            with open(self.path, 'rb') as k_file:
                while True:
                    # For large binary files, reading the entire file at once may consume a lot of memory.
                    # In such cases, it is better to read the file in smaller chunks using read(size).
                    # The file is read in blocks of 40 bytes until no more data is available.
                    chunk = k_file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    # row format: time, lat, lon, tmp, ve, vn, spd, v.lat, v.lon, e.tp
                    # row example: 
                    # 16545.75 39.65458679199219 11.238564491271973 16.808923721313477
                    # 19.44458770751953 10.877525329589844 22.280317306518555 6.941260380699532e-06
                    # 1.0741766345745418e-05 0.0013408786617219448
                    tuple = struct.unpack(FORMAT_STRING, chunk)
                    # Convert to list because Python tuples are immutable
                    self.kfl.append(list(tuple))
                        
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            if self.print_except:
                print(message)
        finally:
            if k_file:
                k_file.close() # Always executes, ensuring the stream is freed

        length = len(self.kfl)
        if length > 1:
            # The first record is a header indicating how many rows were entered
            # (Fortran legacy).
            row = self.kfl[1] # second record.
            self.start_time = row[0]
            row = self.kfl[length - 1] # jump to the final record.
            self.end_time = row[0]

        # A 2D array.
        # It holds the P-File for an specific buoy.
        return self.kfl
        
    # This function write drifter data into the binary (unformatted) direct-access
    # file called k<BUOY_ID>.dat, while creating a timestamped backup copy beforehand.
    def wkfl(self, k_file):
        common = CommonFunctions()
        # Automatically create a timestamped backup copy of the existing P-File.
        backup_file = common.create_timestamped_backup(self.path)
        if (backup_file):
            print('\n' + "K-File backup created:", backup_file, "with today's date/time.")
        
        file = None
        # Flatten the 2D list into a 1D list
        flat_data = [item for row in k_file for item in row]
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
