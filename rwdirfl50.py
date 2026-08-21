#!/usr/bin/python

# Programer CG August 2026

from database_manager import DatabaseManager
from file_manager import FileManager

# This is a main program that reads the DIR-File into memory
# and exports the formatted data into a text file named dirflout3.out.
def main():
    directory_file = []
    # Loads the directory file into memory
    db_manager = DatabaseManager()
    # Returns a 2D array of double-precision floating-point numbers.
    directory_file = db_manager.select_all_dirfl()
    
    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n')
    print("Number of DIR-File records: ", len(directory_file))

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
    # The 15th column in DIR-File represents the drogue-off date.
    # From 16th column to 21st column in DIR-File represents the instrument sensor status flags.
    # The 22th column in DIR-File represents the death code.
    
    # An integer variable tracking the total number of valid records read.
    cnt = 0
    output_lines = []
    for row in directory_file:
        # Validation check for a valid buoy ID.
        if int(row[0]) > 0:
            cnt += 1
            # Creates formatted.
            # It converts columns 1-4, 11-14, and 22 into integers while 
            # keeping the remaining columns as floating-point decimals.
            # Columns 16 through 21 are skipped entirely.
            record = '{:>7}'.format(str(cnt))
            record += '{:>16}'.format(str(int(row[0])))
            record += '{:>8}'.format(str(int(row[1])))
            record += '{:>6}'.format(str(int(row[2])))
            record += '{:>3}'.format(str(int(row[3])))
            record += '{:>9}'.format(str(f"{row[4]:.2f}"))
            record += '{:>8}'.format(str(f"{row[5]:.2f}"))
            record += '{:>8}'.format(str(f"{row[6]:.2f}"))
            record += '{:>10}'.format(str(f"{row[7]:.2f}"))
            record += '{:>8}'.format(str(f"{row[8]:.2f}"))
            record += '{:>8}'.format(str(f"{row[9]:.2f}"))
            record += '{:>5}'.format(str(int(row[10])))
            record += '{:>5}'.format(str(int(row[11])))
            record += '{:>5}'.format(str(int(row[12])))
            record += '{:>5}'.format(str(int(row[13])))
            record += '{:>10}'.format(str(f"{row[14]:.2f}"))
            record += '{:>2}'.format(str(int(row[21])))

            output_lines.append(record)
            
    if len(output_lines) > 0:
        file_name = "dirflout3.out"
        fl_manager = FileManager()
        fl_manager.write_list('', file_name, output_lines) 
        # Prints a success message to the command line terminal telling the user the file is ready.
        print(f"{'The file '}{file_name}{' was created.'}")
        print('\n')       
    
if __name__ == '__main__':
    main()