#!/usr/bin/python

# Programer CG August 2026

from file_manager import FileManager
from database_manager import DatabaseManager
from p_file import PFile
from k_file import KFile

# This cross-checks time fields across three data sources.
# It flags discrepancies where start time or end time differ by more than 1 day
# between DIR-File, P-File and K-File.
# It writes the comparison mismatch it finds into an output text file.
def subchkstet(directory_file):
    # File to write logging summaries.
    file_name = "chkstet.out"
    results = []
    record = ''

    # Reads existing formatted text file containing the target IDs.
    print('\n')
    print(f"{' ' * 9}{'Enter complete file name with IDs to check,'}")
    input_file = input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/ids.lis): '}")
    print('\n')
    results.append(' ')
                    
    file = None
    file_manager = FileManager()
    input_file_path = file_manager._resolve_path(input_file)
    try:
        # input_file format: buoy_id.
        with open(input_file_path, "r", encoding = "utf-8") as file:
            lines = [line.rstrip() for line in file]

            db_manager = DatabaseManager()
            for buoy_id in lines:
                # Looks for the ID in the DIR-File.
                idx = db_manager.select_row_number_dirfl(int(buoy_id))
                if (idx >= 0 ):
                    pfl             = PFile(str(int(buoy_id)))
                    p_file          = pfl.rpfl()
                    kfl             = KFile(str(int(buoy_id)))
                    k_file          = kfl.rkfl()

                    if len(p_file) > 0 and len(k_file) > 0:
                        # P-File and K-File were found.
                        pfl_start_time  = pfl.get_start_time()
                        pfl_end_time    = pfl.get_end_time()

                        kfl_start_time  = kfl.get_start_time()
                        kfl_end_time    = kfl.get_end_time()

                        drfl_row        = directory_file[idx]
                        # The 5th column in DIR-File represents the deployment timestamp.
                        # The 8th column in DIR-File represents the timestamp of the last successful signal fix.
                        drfl_start_time = drfl_row[4]
                        drfl_end_time   = drfl_row[7]

                        # Calculates the absolute variation.
                        p_start_time_diff   = abs (drfl_start_time - pfl_start_time)
                        k_start_time_diff   = abs (drfl_start_time - kfl_start_time)
                        p_end_time_diff     = abs (drfl_end_time - pfl_end_time)
                        k_end_time_diff     = abs (drfl_end_time - kfl_end_time)

                        # Times differ by more than 1 day?
                        if p_start_time_diff > 1:
                            record = '{:>16}'.format(buoy_id)
                            record += ' st dir=' + f"{drfl_start_time:10.3f}"
                            record += ' st p=' + f"{pfl_start_time:10.3f}"
                            record += ' chk st in dir,p, dif=' + '{:>4}'.format(int(p_start_time_diff))
                            results.append(record)
                            print(record)
                        if p_end_time_diff > 1:
                            record = '{:>16}'.format(buoy_id)
                            record += ' et dir=' + f"{drfl_end_time:10.3f}"
                            record += ' et p=' + f"{pfl_end_time:10.3f}"
                            record += ' chk et in dir,p, dif=' + '{:>4}'.format(int(p_end_time_diff))
                            results.append(record)
                            print(record)
                        if k_start_time_diff > 1:
                            record = '{:>16}'.format(buoy_id)
                            record += ' st dir=' + f"{drfl_start_time:10.3f}"
                            record += ' st k=' + f"{kfl_start_time:10.3f}"
                            record += ' chk st in dir,k, dif=' + '{:>4}'.format(int(k_start_time_diff))
                            results.append(record)
                            print(record)
                        if k_end_time_diff > 1:
                            record = '{:>16}'.format(buoy_id)
                            record += ' et dir=' + f"{drfl_end_time:10.3f}"
                            record += ' et k=' + f"{kfl_end_time:10.3f}"
                            record += ' chk et in dir,k, dif=' + '{:>4}'.format(int(k_end_time_diff))
                            results.append(record)
                            print(record)
                else:
                    # Buoy ID wasn't found in DIR-File
                    print(f"Error: {buoy_id} not found in DIR-File. Skip to the next ID.")
    except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
    finally:
        if file:
            file.close() # Always executes, ensuring the stream is freed
    
    fl_manager = FileManager()
    fl_manager.write_list('', file_name, results)
    if len(results) > 0:
        text = f"{' file: '}{file_name}{' created with results'}"
    else:
        text = f"{' file: '}{file_name}{' is empty, no difference found.'}"
    print('\n')
    print(text)
