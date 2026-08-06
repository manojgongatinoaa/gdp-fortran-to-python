#!/usr/bin/python

# Programer: CG August 2026

import os

from file_manager import FileManager

# This function automates the creation of a shell script (krignew.sh).
# This script acts as a "runstream" to feed inputs into an external program called krignew.exe.
def crrunkrig():
    print('\n')
    print(f"{' ' * 9}{'Enter the complete file name where IDs to process are,'}")
    ids_lis = input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/dead_ids.lis): '}")

    print('\n')
    print(f"{' ' * 9}{'Enter directory where runstream will go,'}")
    destination_path = input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/): '}")
    # Check if the last character is not a slash.
    if ((destination_path) and (not destination_path.endswith('/'))):
        destination_path += "/"
    
    lines = []
    fl_manager = FileManager()
    try:
        lines = fl_manager.read_text(ids_lis).split() # plain text, must already exist
        # Convert all items to absolute values and 
        # format them as a right-aligned, 15-digit integer
        abs_numbers = ['{:>15}'.format(str(abs(int(x)))) for x in lines]
        
        if (len(abs_numbers) > 0):
            runstream_file = destination_path + "krignew.sh"

            header = []
            header.append("#!/bin/sh") # standard Linux shebang line
            header.append(" cd " + destination_path + " ") # change directories into destination path
            header.append("/phodnet/drifter/programs/krignew.exe << end > krignew.out") #  execution command for krignew.exe
            # Insert header at the beginning.
            abs_numbers[:0] = header

            food = []
            food.append(" 9999") # serves as a termination signal or exit code for the krignew.exe program.
            food.append("end") # to close the Linux Here Document (<< end), completing the script's input stream.
            # Add food to the end.
            abs_numbers.extend(food)

            # Creates or overwrites the output shell script krignew.sh
            # inside the destination directory.
            fl_manager.write_list('', runstream_file, abs_numbers)
            # Set permissions to 777 (read, write, execute for everyone)
            # making the script executable.
            os.chmod(runstream_file, 0o777)

            print('\n')
            print(f"{'File '}{runstream_file}{' was created.'}")

            print('\n')
            print(f"{'Type the following commands to execute the script,'}")
            print(f"{' ' * 4}{runstream_file}")
            print('\n')
            print(f"{'Output from running krignew.sh is: '}")
            print (f"{' ' * 4}{destination_path}{'krignew.out'}")

    except FileNotFoundError as e:
        print('\n')
        print(f"Error: {e}")        

