#!/usr/bin/python

# Programer CG August 2026

from database_manager import DatabaseManager
from file_manager import FileManager
from k_file import KFile

# Verifies whether a corresponding K-File exists for every entry in DIR-File.
# It logs any missing files to an output report.
def check_dirkfl(directory_file):
    # File to write logging summaries.
    file_name = "nokfiles.out"
    results = []
    # Writes a blank line to the top of the output report file.
    results.append(' ')
    record = ''

    print('\n' + "Wait!: Verifying existing K-File..." + '\n')

    db_manager = DatabaseManager()
    # The 1st column in DIR-File represents the buoy ID.
    for row in directory_file:
        buoy_id = str(int(row[0]))
        kfl     = KFile(str(int(buoy_id)), False) # no print exception message if the K-File doesn't exist
        k_file  = kfl.rkfl()
        if len(k_file) == 0:
            record = f"{' no file for id '}{'{:>23}'.format(buoy_id)}"
            results.append(record)
            print(record)

    print('\n')
    fl_manager = FileManager()
    fl_manager.write_list('', file_name, results)
    if len(results) > 0:
        text = f"{' file: '}{file_name}{' created with results'}"
    else:
        text = f"{' file: '}{file_name}{' is empty, all WMO number are currently assigned'}"
    print(text)
