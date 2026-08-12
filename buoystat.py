#!/usr/bin/python

# Programer: CG August 2026

from pathlib import Path

from database_manager import DatabaseManager
from file_manager import FileManager
from common import CommonFunctions
from menu import Menu

g_exp_no = ''
g_destination_directory = ''
g_directory_file = []
g_jd_to_date = False
# A counter tracking how many output reports have been generated
# during the execution session.
g_count = 0
# List of file's path just written.
g_created_files = []

def write_file(file_bstatX):
    if len(file_bstatX) > 0:
        global g_count
        g_count += 1
        overwrite = True
        while True:
            file_name = f"{'bstat'}{g_count}{'.lis'}"
            print('\n' + "Wait!: File " + file_name + " has been created...")
            file_path = f"{g_destination_directory}{file_name}"

            path = Path(file_path)
            # Check if the path exists (can be a file OR a directory)
            if path.exists():
                answer = input(f"{' ' * 9}{'overwrite '}{file_path}{' ? '}")
                if (answer.upper() == 'Y'):
                    overwrite = True
                else:
                    overwrite = False
                    g_count += 1
            else:
                overwrite = True

            if overwrite:
                # WRITE FILE
                fl_manager = FileManager()
                fl_manager.write_list('', file_path, file_bstatX)
                global g_created_files
                g_created_files.append(file_name)
                break

# ***********************
# *** list statistics ***
# ***********************

def format_record_calendar_date(row):
    # Convert Julian Day to calendar date.
    common = CommonFunctions()
    date = common.jd_to_date_base(row[4])
    # Format into a string format
    mm          = '{:>6}'.format(f"{date[1]}")
    dd          = '{:>5}'.format(f"{int(date[2])}")
    yyyy        = '{:>5}'.format(f"{date[0]}")
    start_time  = mm + dd + yyyy

    if (row[7] > 0.0):
        # Only if buoy was killed, convert the date.
        date = common.jd_to_date_base(row[7])
        # Format into a string format
        mm          = '{:>7}'.format(f"{date[1]}")
        dd          = '{:>5}'.format(f"{int(date[2])}")
        yyyy        = '{:>5}'.format(f"{date[0]}")
        end_time    = mm + dd + yyyy
    else:
        # Format into a string format
        mm          = '{:>7}'.format(f"{0}")
        dd          = '{:>5}'.format(f"{0}")
        yyyy        = '{:>5}'.format(f"{0}")
        end_time    = mm + dd + yyyy

    if (row[14] > 0.0):
        # Only if drogue was lost, convert the date
        date = common.jd_to_date_base(row[14])
        # Format into a string format
        mm              = '{:>7}'.format(f"{date[1]}")
        dd              = '{:>5}'.format(f"{int(date[2])}")
        yyyy            = '{:>5}'.format(f"{date[0]}")
        drogue_off_time = mm + dd + yyyy
    else:
        # Format into a string format
        mm              = '{:>7}'.format(f"{0}")
        dd              = '{:>5}'.format(f"{0}")
        yyyy            = '{:>5}'.format(f"{0}")
        drogue_off_time = mm + dd + yyyy

    # Format the record to be written
    record = '{:>16}'.format(str(int(row[0])))
    record = record + start_time
    record = record + end_time
    record = record + drogue_off_time

    return record

def format_record_julian_date(row):
    # Format the record to be written
    record = '{:>18}'.format(str(int(row[0])))
    record = record + '{:>7}'.format(str(int(row[4])))
    record = record + '{:>7}'.format(str(int(row[7])))
    record = record + '{:>7}'.format(str(int(row[14])))

    return record

def create_record(idx, row, jd_to_date):
    # Record format:
    #                              date drogue buoy life  # days
    #    id  start date   end date   lost     (days)    drogue on     exp#
    if len(row) > 21:
        # The 1nd column in DIR-File represents the buoy ID.
        # The 3rd column in DIR-File represents the experiment  number.
        # The 5th column in DIR-File represents the deployment timestamp.
        # The 8th column in DIR-File represents the timestamp of the last successful signal fix.
        # The 15th column in DIR-File represents the drogue-off date.
        # The 22th column in DIR-File represents the death code.

        start_time      = str(int(row[4]))
        end_time        = str(int(row[7]))
        drogue_off_time = str(int(row[14]))

        # Converts floating-point values into standard integers for processing:
        # start day, end day, drogue-off day, and death code.
        istart_date      = int(row[4])
        iend_date        = int(row[7])
        idrogue_off_date = int(row[14])
        ideath_code      = int(row[21])
                
        # Finding the delta between start and end days.
        days_in_trajectory = iend_date - istart_date
        # Sets a character flag based on buoy's status
        if ideath_code > 0:
            ct = '  ' # buoy is dead
        else:
            ct = ' *' # buoy is alive

        # If drogue-off day is a positive value (meaning the drogue was confirmed
        # lost during the deployment), it calculates how many days it lasted by 
        # subtracting the start day.
        if idrogue_off_date > 0:
            days_with_drogue_on = idrogue_off_date - istart_date
            cd = '  ' # drogue lost
            if days_with_drogue_on < 0:
                # If the math produces a negative value, it defaults it to 0.
                days_with_drogue_on = 0 # buoys with drogue-off day = 1-1-79
        else:
            # If drogue-off date was 0 or negative (meaning the drogue never came off),
            # the drogue duration is calculated as the full lifespan of the buoy, and 
            # cd is flagged with an asterisk (*) to show it stayed attached.
            days_with_drogue_on = iend_date - istart_date
            cd = ' *' # drogue still on

        # Switch formatting based on whether you want standard
        # calendar dates (Month Day Year) or Julian days.
        if (jd_to_date):
            record = '{:>8}'.format(str(idx))
            record = record + format_record_calendar_date(row)
            record = record + '{:>11}'.format(str(days_in_trajectory) + ct)
            record = record + '{:>10}'.format(str(days_with_drogue_on) + cd)
            record = record + '{:>14}'.format(str(int(row[2])))
        else:
            record = format_record_julian_date(row)
            record = record + '{:>9}'.format(str(days_in_trajectory) + ct)
            record = record + '{:>10}'.format(str(days_with_drogue_on) + cd)
            record = record + '{:>11}'.format(str(int(row[2])))
    
    return record, days_in_trajectory, days_with_drogue_on # Returns a tuple

def create_header():
    header_star = "*" * 73 + '\n'

    header_2_3 = f"{' ' * 30}{'date drogue buoy life  # days'}" + '\n'
    header_2_3 = header_2_3 + f"{' ' * 5}{'id'}" + f"{' ' * 2}{'start date'}"
    header_2_3 = header_2_3 + f"{' ' * 3}{'end date'}" + f"{' ' * 3}{'lost'}"
    header_2_3 = header_2_3 + f"{' ' * 5}{'(days)'}" + f"{' ' * 4}{'drogue on'}"
    header_2_3 = header_2_3 + f"{' ' * 5}{'exp#'}" + '\n'
    
    return '\n' + ' ' + header_star + header_2_3 + ' ' + header_star

def create_food(lastot, ndtot):
    food_star = "*" * 80 + '\n'

    slastot = '{:>8}'.format(str(lastot))
    sndtot = '{:>10}'.format(str(ndtot))
    total = f"{' ' * 35}{'total'}{slastot}{sndtot}" + '\n\n'

    note = "* = buoy still alive or drogue still on" + '\n\n'
    note = note + "date drogue lost = 1-1-79 is used when drogue sensor" + '\n'
    note = note + "never worked, therefore, drogue lost day could not" + '\n'
    note = note + "be determined" + '\n'

    return '\n' + food_star + total +  food_star + note

# This function formats and writes records from DIR-File like buoy id,
# start time, end timed, drogue-off date, etc) to a specified text file
# listing by experiment number.
# It switches formatting based on whether you want standard calendar dates
# (Month/Day/Year) or Julian days.
def dprint_by_experiment(exp_no, directory_file, jd_to_date):  
    file_bstatX = []
    # Start with the header.
    file_bstatX.append(create_header())
    
    # Formats and creates records
    lastot = 0
    ndtot = 0
    idx = 1
    for row in directory_file:
        if (len(row) > 21):
            # If entered experiment number is equals 9999 it means 
            # the user requested all experiment number.
            # If the user requested a specific experiment number, it
            # checks if this buoy's experiment column matches.
            if ((int(exp_no) == 9999) or ((int(exp_no) == int(row[2])))):
                record, days_in_trajectory, days_with_drogue_on = create_record(idx, row, jd_to_date)
                file_bstatX.append(record)
                # Adds the current buoy's lifespan days and drogue active days
                # to global accumulators to calculate experiment-wide metrics.
                lastot = lastot + days_in_trajectory
                ndtot = ndtot + days_with_drogue_on
        idx += 1
    
    # Finish with the food
    file_bstatX.append(create_food(lastot, ndtot))

    return file_bstatX

def enter_destination_path():
    print('\n')
    print(f"{' ' * 9}{'Enter directory where the files bstat*.lis will go,'}")
    global g_destination_directory
    g_destination_directory = input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/): '}")
    # Check if the last character is not a slash.
    if ((g_destination_directory) and (not g_destination_directory.endswith('/'))):
        g_destination_directory += "/"

def enter_exp_no() -> str:
    global g_directory_file
    if (len(g_directory_file) == 0):
        # Loads the directory file
        db_manager = DatabaseManager()
        g_directory_file = db_manager.select_all_dirfl()
        
        # Prints a message to the console showing how many rows were successfully loaded.
        print('\n')
        print("Number of DIR-File records: ", len(g_directory_file))

    print('\n')
    global g_exp_no
    g_exp_no = input(f"{' ' * 9}{'Enter experiment number to search for, 9999 if all of them: '}")

# Prints out to screen file just written
def Display_created_files():
    fl_manager = FileManager()
    for file_name in g_created_files:
        file_path = Path(file_name)
        # Check if the path exists (can be a file OR a directory)
        if file_path.exists():
            print(fl_manager.read_text(file_name))

def list_records():
    # Creates bstat*.lis file
    global g_directory_file
    # Formats and writes records
    file_bstatX = dprint_by_experiment(g_exp_no, 
                                g_directory_file, 
                                g_jd_to_date)
    write_file(file_bstatX)

def return_function(choice):
    if (choice == 1):
        # 1. list statistics
        list_records() # create file bstat*.lis
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            if (len(g_created_files) > 0):
                # Before it leaves list_by_experiment_menu().
                print('\n')
                answer = input(f"{' ' * 9}{'Do you want to display the created files on the screen? (y/n)' }")
                if (answer.upper() == 'Y'):
                    Display_created_files()

            print("Exit!" + '\n')

# This function computes statistics of buoys. 
# It filters buoys by a user-specified experiment number, computes how many days 
# each buoy lasted, determines how long its drogue stayed attached, writes these
# statistics to a structured text file, and can optionally display the results to
# the screen.
# Parameter:
#   jd_to_date     - Flag controlling date formatting. If True, timestamps convert 
#                    to Month/Day/Year. If False, they print as raw decimals.
def buoystat(jd_to_date) -> int:
    enter_destination_path()
    enter_exp_no()
    
    global g_jd_to_date
    g_jd_to_date = jd_to_date
    
    text = "M E N U (statistics by experiment number)"
    title = '\n' + f"{' ' * 9}{text}"  + '\n'
    title = title + f"{' ' * 9}{'=' * len(text)}"
    menu_dictionary = {
        "1. ": "continue",
    }
    last_option_description = "stop"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()
