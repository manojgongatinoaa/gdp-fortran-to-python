#!/usr/bin/python

# Programer CG August 2026

from file_manager import FileManager
from k_file import KFile

# Compares the drogue-off date in DIR-File to the end time in K-File.
# If the drogue-off date in the DIR-File is greater than the last entry in the K-File,
# it flags the discrepancy, calculates the absolute time difference, logs it to a file
# named chkdrokfl.out, and prints it to the console.
def subchkdoffkfl(directory_file):
    # File to write logging summaries.
    file_name = "chkdrokfl.out"
    results = []
    # Writes a blank line to the top of the output report file.
    results.append(' ')
    record = ''

    print('\n' + "Wait!: Verifying existing K-File..." + '\n')

    # The 1st column in DIR-File represents the buoy ID.
    # The 5th column in DIR-File represents the deployment timestamp.
    # The 8th column in DIR-File represents the timestamp of the last successful signal fix.
    # The 15th column in DIR-File represents the drogue-off date.
    for row in directory_file:
        buoy_id = str(int(row[0]))
        kfl     = KFile(buoy_id)
        k_file  = kfl.rkfl()
        if len(k_file) > 0:
            drogue_off_date = row[14]
            kfl_end_time    = kfl.get_end_time() # gets the value from the very last record.
            # Checks if the K-File's last time is strictly less than the DIR-File's
            # recorded drogue-off time.
            if int(kfl_end_time) < int(drogue_off_date):
                total_time_diff = abs(kfl_end_time - drogue_off_date)
                start_time      = row[4]
                end_time        = row[7]

                record = '{:>22}'.format(buoy_id)
                record += f"{start_time:12.3f}"
                record += f"{end_time:15.3f}"
                record += f"{drogue_off_date:15.3f}"
                record += f"{kfl_end_time:15.3f}"
                record += f"{total_time_diff:15.3f}"
                results.append(record)
                print(record)
        else:
            print(f"{' no k-file for this id '}{buoy_id}")
    print('\n')
    fl_manager = FileManager()
    fl_manager.write_list('', file_name, results)
    if len(results) > 0:
        text = f"{' file: '}{file_name}{' created with results'}"
    else:
        text = f"{' file: '}{file_name}{' is empty, no discrepancy found'}"
    print(text)
