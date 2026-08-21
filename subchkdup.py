#!/usr/bin/python

# Programer CG August 2026

from file_manager import FileManager
from common import CommonFunctions

def get_formatted_record(row):
    # The 1st column in DIR-File represents the buoy ID.
    # The 2nd column in DIR-File represents the WMO number.
    # The 3rd column in DIR-File represents the experiment  number.
    # The 4th column in DIR-File represents the buoy type classification code.
    # The 5th column in DIR-File represents the deployment timestamp.
    # The 6th column in DIR-File represents the deployment latitude coordinate.
    # The 7th column in DIR-File represents the deployment longitude coordinate.
    # The 8th column in DIR-File represents the timestamp of the last successful signal fix.
    # The 9th column in DIR-File represents the last recorded latitude coordinate.
    # The 10th column in DIR-File represents the last recorded longitude coordinate.
    # The 11th column in DIR-File represents the southernmost latitude boundary limit.
    # The 12th column in DIR-File represents the northernmost latitude boundary limit.
    # The 13th column in DIR-File represents the westernmost longitude tracking.
    # The 14th column in DIR-File represents the easternmost longitude tracking.
    # The 15th column in DIR-File represents the drogue off date.
    # The 22th column in DIR-File represents the death code.
    record = '{:>16}'.format(str(int(row[1])))
    record += '{:>8}'.format(str(int(row[2])))
    record += '{:>6}'.format(str(int(row[3])))
    record += '{:>3}'.format(str(int(row[4])))
    record += '{:>9}'.format(str(f"{row[5]:.2f}"))
    record += '{:>7}'.format(str(f"{row[6]:.2f}"))
    record += '{:>8}'.format(str(f"{row[7]:.2f}"))
    record += '{:>6}'.format(str(int(row[8])))
    record += '{:>7}'.format(str(f"{row[9]:.2f}"))
    record += '{:>8}'.format(str(f"{row[10]:.2f}"))
    record += '{:>6}'.format(str(int(row[11])))
    record += '{:>6}'.format(str(int(row[12])))
    record += '{:>7}'.format(str(int(row[13])))
    record += '{:>7}'.format(str(int(row[14])))
    record += '{:>6}'.format(str(int(row[15])))
    record += '{:>2}'.format(str(int(row[22])))

    return record

# Searches DIR-File to find and log duplicate record IDs.
# It writes the details of any matching pairs it finds into an output text file.
def subchkdup(directory_file):
    # File to write logging summaries.
    file_name = "chkdup.out"
    results = []
    record = ''

    # Writes a blank line to the top of the output file.
    results.append('\n')
    print('\n')
    column = 0 # by buoy ID
    common = CommonFunctions()
    duplicates = common.find_duplicate_rows_by_col(directory_file, column)
    #print(*duplicates, sep ='\n')
    num = 2
    even = True
    for row in duplicates:
        if (len(row) > 22):
            if (num % 2 == 0):
                even = True
            else:
                # Odd
                even = False
                        
            if even:
                record = f"{' duplicate record found for id '}{int(row[1])}" + '\n'
            else:
                # Odd
                record = ''
            record += '{:>5}'.format(str(row[0]+1))
            record += get_formatted_record(row)

            if not even:
                record += '\n'
            results.append(record)
            print(record)
            num += 1
        
    fl_manager = FileManager()
    fl_manager.write_list('', file_name, results)
    if len(results) > 0:
        text = f"{' file: '}{file_name}{' created with results'}"
    else:
        text = f"{' file: '}{file_name}{' is empty, no duplicates were found.'}"
    print(text)

