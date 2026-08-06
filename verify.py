#!/usr/bin/python

# Programer CG August 2026

import datetime

from helper import Menu
from common import CommonFunctions
from directory_file import DirectoryFile

g_row = []
g_change_record = False
g_jd_to_date = False
g_menu1 = None
g_menu2 = None
g_menu3 = None

def set_first_menu_dictionary():
    # The 1nd column in DIR-File represents the buoy ID.
    # The 2nd column in DIR-File represents the WMO number.
    # The 3rd column in DIR-File represents the experiment  number.
    # The 4th column in DIR-File represents the buoy type classification code.
    # The 5th column in DIR-File represents the deployment timestamp.
    # The 6th column in DIR-File represents the deployment latitude coordinate.
    # The 7th column in DIR-File represents the deployment longitude coordinate.
    # The 8th column in DIR-File represents the timestamp of the last successful signal fix.
    # The 9th column in DIR-File represents the last recorded latitude coordinate.
    # The 10th column in DIR-File represents the last recorded longitude coordinate.
    start_time  = str(f"{g_row[4]:.3f}")
    end_time    = str(f"{g_row[7]:.3f}")
    if (g_jd_to_date):
        # Convert Julian Day to date.
        common = CommonFunctions()
        date = common.jd_to_date_base(g_row[4]) # Convert Julian Day to date.
        # Format each sub-list into a "YYYY/MM/DD.DD" string format
        start_time = f"{date[0]}/{date[1]:02d}/{date[2]:04.2f}"
        if (g_row[7] > 0.0): # If ending date greater than 0, convert.
            # Only if buoy was killed, convert the date.
            date = common.jd_to_date_base(g_row[7]) # Convert Julian Day to date.
            # Format each sub-list into a "YYYY/MM/DD.DD" string format
            end_time = f"{date[0]}/{date[1]:02d}/{date[2]:04.2f}"
        else:
            end_time = '0000/0/0'
    menu_dictionary = {
        " 1. ": "buoy id ............ " + str(int(g_row[0])),
        " 2. ": "wmo #............... " + str(int(g_row[1])),
        " 3. ": "exp # .............. " + str(int(g_row[2])),
        " 4. ": "buoy type .......... " + str(int(g_row[3])),
        " 5. ": "deployment date .... " + start_time,
        " 6. ": "deployment lat ..... " + str(f"{g_row[5]:.3f}"),
        " 7. ": "deployment lon ..... " + str(f"{g_row[6]:.3f}"),
        " 8. ": "date of last fix ... " + end_time,
        " 9. ": "last latitude ...... " + str(f"{g_row[8]:.3f}"),
        "10. ": "last longitude...... " + str(f"{g_row[9]:.3f}")
    }
    g_menu1.set_dictionary(menu_dictionary)

def set_second_menu_dictionary():
    # The 11th column in DIR-File represents the southernmost latitude boundary limit.
    # The 12th column in DIR-File represents the northernmost latitude boundary limit.
    # The 13th column in DIR-File represents the westernmost longitude tracking.
    # The 14th column in DIR-File represents the easternmost longitude tracking.
    # The 15th column in DIR-File represents the drogue off date.
    drogue_off_time  = str(f"{g_row[14]:.3f}")
    if (g_jd_to_date):
        # Convert Julian Day to date.
        if (g_row[14] > 0.0):
            # Only if buoy lost its drogue, convert the date 
            common = CommonFunctions()
            date = common.jd_to_date_base(g_row[14]) # Convert Julian Day to date.
            # Format each sub-list into a "YYYY/MM/DD.DD" string format
            drogue_off_time = f"{date[0]}/{date[1]:02d}/{date[2]:04.2f}"
        else:
            drogue_off_time = '0000/0/0'

    menu_dictionary = {
        "11. ": "southernmost lat ....... " + str(int(g_row[10])),
        "12. ": "northernmost lat ....... " + str(int(g_row[11])),
        "13. ": "westernmost longitude... " + str(int(g_row[12])),
        "14. ": "easternmost longitude... " + str(int(g_row[13])),
        "15. ": "date drogue lost........ " + drogue_off_time
    }
    g_menu2.set_dictionary(menu_dictionary)

def set_third_menu_dictionary():
    # From 16th column to 21st column in DIR-File represents the instrument sensor status flags.
    # The 22nd column in DIR-File represents the drogue deactivation code.
    menu_dictionary = {
        "16. ": "sensor .......... " + str(int(g_row[15])),
        "17. ": "sensor .......... " + str(int(g_row[16])),
        "18. ": "sensor .......... " + str(int(g_row[17])),
        "19. ": "sensor .......... " + str(int(g_row[18])),
        "20. ": "sensor .......... " + str(int(g_row[19])),
        "21. ": "sensor .......... " + str(int(g_row[20])),
        "22. ": "type of death.... " + str(int(g_row[21]))
    }
    g_menu3.set_dictionary(menu_dictionary)

def evaluate_polar_compass():
    global g_row
    west   = 0.0
    east   = 0.0
    if (g_row[13] > 0.0 and g_row[12] < 0.0):
        west = g_row[12]
        east = g_row[13]
    if (g_row[13] > 0.0 and g_row[12] > 0.0):
        west = g_row[13]
        east = g_row[12]
    if (g_row[13] < 0.0 and g_row[12] < 0.0):
        west = g_row[13]
        east = g_row[12]
    if (int(g_row[13]) == 0 and int(g_row[12]) == 0):
        west = g_row[13]
        east = g_row[12]

    g_row[12] = west # westernmost
    g_row[13] = east # easternmost
    
def return_function(choice):
    if (choice > 0):
        if (g_change_record):
            new_value = float(0)
            global g_row
            user_input = input(f"{' ' * 9}{'Enter new value: '}")
            common = CommonFunctions()
            if (not common.is_float(user_input)):
                if (g_jd_to_date == True and (choice == 5 or choice == 8 or choice ==15)):
                    split = user_input.split('/')
                    if (len(split) > 2):
                        year = int(split[0])
                        month = int(split[1])
                        day = float(split[2])

                        if (common.validate_date_with_float_day(year, month, day)):
                            new_value = common.date_to_jd(year, month, day)
                        else:                    
                            print(f"Invalid date or format! Please use 2026/12/26.")
            else:
                new_value = float(user_input)

            g_row[choice-1] = new_value # make the change one by one.

            if (choice == 13 or choice == 14):
                # Evaluates polar compass orientation signs across columns 13 and 14 
                # to determine directional tracking arrays
                evaluate_polar_compass()

            if (choice >= 1 and choice <= 10):
                set_first_menu_dictionary()
            elif(choice >= 11 and choice <= 15):
                set_second_menu_dictionary()
            elif(choice >= 16 and choice <= 22):
                set_third_menu_dictionary()
    else:
        if (choice < 0):
            print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")

def create_menu1():
    title = '\n' + f"{' ' * 9}{'Verify Record'}"  + '\n'
    title = title + f"{' ' * 9}{'=========================='}"
    if (not g_change_record):
        last_option_description = "to continue"
    else:
        last_option_description = "no more changes"

    global g_menu1
    g_menu1 = Menu(title, None, last_option_description, return_function)
    set_first_menu_dictionary()
    g_menu1.loop()

def create_menu2():
    title = '\n' + f"{' ' * 9}{'Verify Record'}"  + '\n'
    title = title + f"{' ' * 9}{'=========================='}"
    if (not g_change_record):
        last_option_description = "to continue"
    else:
        last_option_description = "no more changes"

    global g_menu2
    g_menu2 = Menu(title, None, last_option_description, return_function)
    set_second_menu_dictionary()
    g_menu2.loop()

def create_menu3():
    # From 16th column to 21st column in DIR-File represents the instrument sensor status flags.
    # The 22nd column in DIR-File represents the drogue deactivation code.
    title = '\n' + f"{' ' * 9}{'Verify Record'}"  + '\n'
    title = title + f"{' ' * 9}{'=========================='}"
    if (not g_change_record):
        last_option_description = "to continue"
    else:
        last_option_description = "no more changes"

    global g_menu3
    g_menu3 = Menu(title, None, last_option_description, return_function)
    set_third_menu_dictionary()
    g_menu3.loop()

# This function displays buoy records (such as coordinates, 
# deployment tracking dates, sensor flags, and operational status)
# stored in a DIR-File.
# Based on the value of julian parameter, it optionally translates raw
# julian/decimal timestamps into formatted calendar dates. It runs an
# interactive terminal menu allowing a user to overwrite individual data
# fields on the fly.
# Parameter:
#   record         - DIR-File record to verify.
#   jd_to_date     - Flag controlling date formatting. If True, timestamps convert 
#                    to Month/Day/Year. If False, they print as raw decimals.
#   change_record  - Flag to distinguish whether the record needs to be changed or is 
#                    merely being displayed.
def verify(record, jd_to_date, change_record):
    # DIR-File row example: 
    # 300534064897810.0, 4401656.0, 2222.0, 48.0, 17201.041015625,
    # 43.189998626708984, -28.010000228881836, 17261.75, 41.73809814453125, -27.218000411987305,
    # 41.0, 44.0, -29.0, -27.0, 17201.041015625,
    # 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0

    # Buoy ID was found in DIR-File
    # Makes copies of DIR-File's row.
    old_row = record.copy()
    global g_row
    g_row = old_row.copy()

    global g_jd_to_date
    g_jd_to_date = jd_to_date

    global g_change_record
    g_change_record = change_record

    create_menu1()
    create_menu2()
    create_menu3()

    return g_row

