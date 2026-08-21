#!/usr/bin/python

# Programer: CG August 2026

from datetime import datetime

from common import CommonFunctions
from database_manager import DatabaseManager
from menu import Menu
from verify import verify

g_jd_to_date = False
g_new_row = []
g_menu = None

def set_menu_dictionary():
    # The 3rd column in DIR-File represents the experiment  number.
    # The 4th column in DIR-File represents the buoy type classification code.
    # The 5th column in DIR-File represents the deployment timestamp.
    # The 6th column in DIR-File represents the deployment latitude coordinate.
    # The 7th column in DIR-File represents the deployment longitude coordinate.
    # The 15th column in DIR-File represents the drogue off date.
    start_time      = str(f"{g_new_row[4]:.3f}")
    drog_off_date   = str(f"{g_new_row[14]:.3f}")
    if (g_jd_to_date):
        # Convert Julian Day to date.
        common = CommonFunctions()
        if (g_new_row[4] > 0.0): # If deployment date greater than 0, convert.
            date = common.jd_to_date_base(g_new_row[4]) # Convert Julian Day to date.
            # Format each sub-list into a "YYYY/MM/DD.DD" string format
            start_time = f"{date[0]}/{date[1]:02d}/{date[2]:04.2f}"
        else:
            start_time = '0000/0/0'

        if (g_new_row[14] > 0.0): # If droggue-off date greater than 0, convert.
            # Only if the buoy lost the drogue, convert the date .
            date = common.jd_to_date_base(g_new_row[14]) # Convert Julian Day to date.
            # Format each sub-list into a "YYYY/MM/DD.DD" string format
            drog_off_date = f"{date[0]}/{date[1]:02d}/{date[2]:04.2f}"
        else:
            drog_off_date = '0000/0/0'

    text = "M E N U (create)"
    title = '\n' + f"{' ' * 9}{text}"  + '\n'
    title = title + f"{' ' * 9}{'=' * len(text)}"
    menu_dictionary = {
        "1. ": "exp # .............. " + str(int(g_new_row[2])),
        "2. ": "buoy type .......... " + str(int(g_new_row[3])),
        "3. ": "deployment date .... " + start_time,
        "4. ": "deployment lat ..... " + str(f"{g_new_row[5]:.3f}"),
        "5. ": "deployment lon ..... " + str(f"{g_new_row[6]:.3f}"),
        "6. ": "date drogue lost.... " + drog_off_date,
        "7. ": "type of death....... " + str(int(g_new_row[21]))
    }
    g_menu.set_dictionary(menu_dictionary)

def set_sensor_type(buoy_type):
    # From 16th column to 21st column in DIR-File represents 
    # the instrument sensor status flags.
    common = CommonFunctions()
    sensor_type = common.fill_sensor_type_array(int(buoy_type))
    j = 15
    for i in range(len(sensor_type)):
        g_new_row[j] = sensor_type[i]
        j += 1

def return_function(choice):
    if (choice > 0):
        idx = 0
        if (choice >= 1 and choice <= 5):
            idx = choice + 1
        elif (choice == 6):
            idx = 14
        elif (choice == 7):
            idx = 21

        new_value = float(0)
        global g_new_row
        user_input = input(f"{' ' * 9}{'Enter new value: '}")
        common = CommonFunctions()
        if (not common.is_float(user_input)):
            if (g_jd_to_date == True and (choice == 3 or choice == 6)):
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

        g_new_row[idx] = new_value # making the change one by one.

        if (choice == 2 and g_new_row[3] > 0.0): # buoy type
            set_sensor_type(g_new_row[3]) # automatic get sensor type.

        if (choice >= 1 and choice <= 7):
            set_menu_dictionary()
    else:
        if (choice < 0):
            print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")

def create_menu():
    text = "Create Record"
    title = '\n' + f"{' ' * 9}{text}"  + '\n'
    title = title + f"{' ' * 9}{'=' * len(text)}"
    last_option_description = "no more changes"

    global g_menu
    g_menu = Menu(title, None, last_option_description, return_function)
    set_menu_dictionary()
    g_menu.loop()

# This function adds a new record to the DIR-File by entering all information interactively.
# Parameter:
#   jd_to_date     - Flag controlling date formatting. If True, timestamps convert 
#                    to Month/Day/Year. If False, they print as raw decimals.
def create(jd_to_date):
    # Loads the directory file
    db_manager = DatabaseManager()
    directory_file = db_manager.select_all_dirfl()
    
    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n')
    print("Number of DIR-File records: ", len(directory_file), '\n')

    global g_jd_to_date
    g_jd_to_date = jd_to_date

    old_row =  [0.0] * 22 # every element equals 0.0
    global g_new_row # new record to add into the DIR-File
    g_new_row = old_row.copy()

    buoy_id = input(f"{' ' * 9}{'Enter buoy ID to work with: '}")

    # Looks for the ID in the DIR-File.
    db_manager = DatabaseManager()
    idx = db_manager.select_row_number_dirfl(int(buoy_id))
    if (idx >= 0 ):
        # Buoy ID was found in DIR-File
        print('\n')
        print("Entry for " + buoy_id + " already exists in DIR-File.")
        print('\n')
    else:
        # DIR-File row example: 
        # 300534064897810.0, 4401656.0, 2222.0, 48.0, 17201.041015625,
        # 43.189998626708984, -28.010000228881836, 17261.75, 41.73809814453125, -27.218000411987305,
        # 41.0, 44.0, -29.0, -27.0, 17201.041015625,
        # 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0

        # Start filling out the record.
        # The 1st column in DIR-File represents the buoy ID.
        g_new_row[0] = float(buoy_id)

        wmo = db_manager.select_wmo(buoy_id)
        if (wmo > float(0)):
            # The 2nd column in DIR-File represents the WMO number.
            g_new_row[1] = float(wmo)

        create_menu()
        
        change_record = True
        new_row = verify(g_new_row, jd_to_date, change_record)

        if (old_row != new_row):
            common = CommonFunctions()
            error_message = common.validate_dirfl_record(new_row)
            if (error_message == None):  # Record is valid
                # Prints out a log of the buoy's parameters before any changes are applied.
                print('\n')
                old = ", ".join(str(num) for num in old_row)
                print(f"{' ' * 6}" + "Old: " + old)
                # Logs the modified data to the console.
                new = ", ".join(str(num) for num in new_row)
                print(f"{' ' * 6}" + "New: " + new)
                
                # Append the new record in DIR-File.
                directory_file.append(new_row)

                # Update the DIR-File.
                db_manager = DatabaseManager()
                db_manager.update_all_dirfl(directory_file)
                added_records = 1
                print('\n')
                print(f"{'Added records: '}{added_records}" + 
                    f"{' ' * 9}{' Original number of records: '}{len(directory_file) - added_records}" +
                    f"{' ' * 9}{' New number of records: '}{len(directory_file)}")
            else:
                print('\n')
                print(" " + f"{int(new_row[0])}" + " " + error_message)
        else:
            print('\n')
            print(f"{' ' * 6}{'Create Record: No changes'}")
        
