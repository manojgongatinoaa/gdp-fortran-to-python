#!/usr/bin/python

# Programer CG August 2026

# This run the option 2 from crtmpfl.py

from directory_file import DirectoryFile
from tmpfl_file import TmpflFile
from common import CommonFunctions

# Add records found in the directory file but not yet in the tmpfl30.dat file.
def update_tmpfl():
    # tmpfl30.dat format: Drifter ID, Experiment number, Deployment start time, Last good temperature day (end time)

    directory_file = DirectoryFile()
    # Loads the directory file
    dirfl = directory_file.rdirfl50()

    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n')
    print(f"{'Number of DIR-File records: '}{len(dirfl)}")
    
    print('\n')
    print(f"{'Wait!: Updating tmpfl.dat30 ...'}")
    
    tmpfl_file = TmpflFile()
    # Read existing tmpfl30.dat file
    tmpfl30 = tmpfl_file.rtmpfl30()

    new_lines = []
    common = CommonFunctions()
    # Looks for the ID in the DIR-File.
    for row in dirfl:
        # The 1st column in DIR-File represents the drifter ID.
        buoy_id = str(int(row[0])) + "."
        
        if (common.get_id_position_in_tmpfl30(buoy_id, tmpfl30) == -1):
            # buoy ID not found in tmpfl30.dat

            # The 3rd column in DIR-File represents the experiment number.
            experiment_number = str(int(row[2])) + "."
            # The 5th column in DIR-File represents the deployment date.
            start_time = f"{row[4]:.3f}"
            # The 8th column in DIR-File represents the date of last fix.
            end_time =  f"{row[7]:.3f}"

            # Creates new line to add to the tmpfl30.dat file.
            line = '{:>16}'.format(buoy_id)
            line = line + '{:>8}'.format(experiment_number)
            line = line + '{:>12}'.format(start_time)
            line = line + '{:>12}'.format(end_time)

            new_lines.append(line)

    if (len(new_lines) > 0):
        print('\n')
        print("You are adding the following IDs to the tmpfl30.dat file:")
        for line in new_lines:
            tmpfl30.append(line + '\n')
            # Logs the added records to the console.
            print(f"{' ' * 4}{line}")

        # Sorting by buoy ID in ascending order
        delimiter = " "
        column_index = 0  # 0 for first column
        # Sorts the target column as numbers instead of text strings
        tmpfl30.sort(
            key = lambda line: float(line.strip().split(delimiter)[column_index])
            )

        tmpfl_file.wtmpfl30(tmpfl30)
    else:
        print('\n')
        print(f"{' ' * 4}" + "No changes")

    #print(*tmpfl30, sep="\n")

    print('\n')
    print("Ready!")

