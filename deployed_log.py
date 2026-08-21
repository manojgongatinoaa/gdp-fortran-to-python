#!/usr/bin/python

# programer: CG August 2026

from itertools import dropwhile

from constants import DEPLOYED_LOG
from common import CommonFunctions
from file_manager import FileManager
from database_manager import DatabaseManager

# Class to safely and easily manage common deployed.log file operations.
class DeployedLog:
    def __init__(self):
        self.path = DEPLOYED_LOG
        self.deployed_log = []

    # Read deployed.log file: This is acting as the data loader.
    #                         It opens the ASCII deployed.log file, reading the data
    #                         row-by-row and stops automatically when it hits the end
    #                         of valid data.
    #                         This program assumes there are 8 digit IDs in deployed.log file.
    #
    # Return:
    # deployed_log - The deployed.log file
    def rdeployedlog(self):
        db_manager = DatabaseManager()
        self.deployed_log = db_manager.select_all_deployed_log()
        return self.deployed_log

    def rdeployedlog_without_header(self):
        deployed_log = self.rdeployedlog()
        # Remove header, removing elements from the beginning until the condition is met.
        # Condition: The first 4 character are not equal '  ID'.
        result = list(dropwhile(lambda x: x[:4] != "  ID", deployed_log))
        result.pop(0)
        return result

    def get_wmo(self, buoy_id: str):
        wmo = 0
        # It assumes deployed.log has 8 digit IDs.
        # Extract the last 8 characters.
        last_eight = buoy_id[-8:]
        lines = self.rdeployedlog_without_header()
        for line in lines:
            spl = line.split()
            if len(spl) > 1:
                if spl[0] == last_eight:
                    wmo = spl[1]
                    break
        return wmo

    # This function write drifter data into deployed.log file,
    # while creating a timestamped backup copy beforehand.
    def wdeployedlog(self, deployed_log):
        common = CommonFunctions()
        # Automatically create a timestamped backup copy of the existing deployed.log file.
        backup_file = common.create_timestamped_backup(self.path)
        if (backup_file):
            print('\n' + "DIR-File backup created:", backup_file, "with today's date/time.")

        file = None
        try:
            fl_manager = FileManager()
            #file = fl_manager.write_list(' ', self.path, deployed_log)
        except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
        finally:
            if file:
                file.close() # Always executes, ensuring the stream is freed
