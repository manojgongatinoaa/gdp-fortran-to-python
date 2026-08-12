#!/usr/bin/python

# programer: CG August 2026

from constants import TMPFL30_DAT
from file_manager import FileManager

# Class to safely and easily manage common tmpfl30.dat operations.
class TmpflFile:
    def __init__(self):
        self.path = TMPFL30_DAT
        self.header = ""

    def select_all_tmpfl30(self):
        matrix = []
        try:
            file = None
            # /phodnet/drifter/data/files/tmpfl30.dat format: 
            # Drifter ID, Experiment number, Deployment start time, Last good temperature day (end time)
            with open(self.path, "r") as file:
                for line in file:
                    matrix.append(line)
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
            self.header = matrix[0]
            matrix.pop(0)

        return matrix

    # Read tmpfl30.dat file: This is acting as the data loader.
    #                It opens the tmpfl30.dat file, reading the data row-by-row
    #                and stops automatically when it hits the end of valid data.
    #
    # Return:
    # tmpfl30 - The tmpfl30.dat file
    def rtmpfl30(self):
        #db_manager = DatabaseManager()
        tmpfl30 = self.select_all_tmpfl30()
        return tmpfl30

    # This function write drifter data into tmpfl30.dat,
    # while creating a timestamped backup copy beforehand.
    def wtmpfl30(self, tmpfl_file):
        from common import CommonFunctions
        common = CommonFunctions()
        # Automatically create a timestamped backup copy of the existing DIR-File.
        backup_file = common.create_timestamped_backup(self.path)
        if (backup_file):
            print('\n' + "tmpfl30.dat backup created:", backup_file, "with today's date/time.")
        
        # Creates or overwrites tmpfl30.dat file with the provided tmpfl_file list
        fl_manager = FileManager()
        file_path = fl_manager._resolve_path(self.path)
        file_path.parent.mkdir(parents = True, exist_ok = True)

        tmpfl_file.insert(0, self.header)
        file = None
        try:
            with open(self.path, "w") as file:
                for line in tmpfl_file:
                    # Convert each element to string, join with tabs, and add a newline
                    file.write(line)

        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if file:
                file.close() # Always executes, ensuring the stream is freed
