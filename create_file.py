#!/usr/bin/python

# Programer: CG July 2026

from database_manager import DatabaseManager
from directory_file import DirectoryFile
from file_manager import FileManager
from common import CommonFunctions

# Fills the six generic "sensor" flags.   
def fill_sensor_type_array(buoy_type):
    # Sensor-type array to prepare depending the buoy type
    sensor_type = [0.0] * 6 # # Creates [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for i in range(3):
        sensor_type[i] = float(i + 1)   # Elements 1, 2, and 3 are configured with 1.0, 2.0, 3.0.
    if (buoy_type == 9.0):              # If the buoy type is 9.0,
        sensor_type[3] = 9.0            # elements 4, 5, and 6 are configured with 9.0.
        sensor_type[4] = 9.0
        sensor_type[5] = 9.0
    elif (buoy_type == 8.0):            # If the buoy type is 8.0,
        sensor_type[3] = 7.0            # elements 4 and 5 are configured with 7.0.
        sensor_type[4] = 7.0
    elif (buoy_type == 11.0):           # If the buoy type is 11.0 (salinity buoy),
        sensor_type[4] = 9.0            # elements 5 and 6 are configured with 9.0.
        sensor_type[5] = 9.0
    elif (buoy_type == 12.0):           # If the buoy type is 12.0 (barometric/wind),
        sensor_type[3] = 7.0            # element 4 is configured with 7.0,
        sensor_type[4] = 1.0            # element 5 is configured with 1.0.
    elif (buoy_type == 13.0):           # If the buoy type is 13.0 (pure wind),
        sensor_type[4] = 1.0            # element 5 is configured with 1.0.

    return sensor_type

def create_new_records_for_directory_file(input_file, directory_file):
#    print(*input_file, sep ='\n')
    new_records = []
    
    print("Wait!: Entering new records on directory file..." + '\n')

    file = None
    common = CommonFunctions()
    file_manager = FileManager()
    input_file_path = file_manager._resolve_path(input_file)
    try:
        # input_file format: buoy_id, buoy_type, project_number, start_time, start_latitude, start_longitude.
        with open(input_file_path, "r", encoding = "utf-8") as file:
            lines = [line.rstrip() for line in file]

            print("Entered records:")

            # The loop reads a list of modified buoy information out of a raw data text file row by row.
            # For every buoy row found, it looks up where that buoy exists inside the IMEI_LUT_DAT.dat file,
            # craete a new record in the DIR-File, and writes a verification tracking statement out to the terminal.
            for line in lines:
                # split() without arguments automatically handles any consecutive whitespace
                columns = line.strip().split()
                if (len(columns) > 0): # If len(columns) == 0 the line is empty.
                    # Ensure the line has enough data to avoid IndexError
                    if (len(columns) > 5):
                        buoy_id         = float(columns[0])
                        buoy_type       = float(columns[1])
                        project_number  = float(columns[2])
                        start_time      = float(columns[3])
                        start_latitude  = float(columns[4])
                        start_longitude = float(columns[5])
                        
                        # Checks if the deployment timestamp exceeds a valid threshold. 
                        if (start_time > 99999):
                            print('\n')
                            print(f"{'Error: Check '}{input_file_path}{' format.'}")
                            print(f"{' ' * 7}" + str(int(buoy_id)) + ', ' + str(int(buoy_type)) + ', ' + 
                                  str(int(project_number)) + ', ' + str(int(start_time)) + ', ' +
                                  str(int(start_latitude)) + ', ' + str(int(start_longitude)))
                            break
                        
                        # Looks for the ID in the DIR-File.
                        idx = common.get_id_position_in_dirfl(buoy_id, directory_file)
                        if (idx >= 0 ):
                            # Buoy ID was found in DIR-File
                            print(f"{' ' * 4}{'Entry for '}{str(int(buoy_id))}{' already exists in DIR-File. Skip to the nex ID.'}")
                        else:
                            db_manager = DatabaseManager()
                            wmo             = float(db_manager.select_wmo(str(int(buoy_id))))
                            sensor_type     = fill_sensor_type_array(int(buoy_type))
                            zero            = float(0)

                            # Creates new record to add into the directory file.
                            # each record has 22 columns and each number is a 64-bits double (8 bytes). 
                            new_record = []
                            new_record.append(buoy_id)
                            new_record.append(wmo)
                            new_record.append(project_number)
                            new_record.append(buoy_type)
                            new_record.append(start_time)
                            new_record.append(start_latitude)
                            new_record.append(start_longitude)
                            new_record.append(zero) # end_time
                            new_record.append(zero) # end_latitude
                            new_record.append(zero) # end_longitude
                            new_record.append(zero) # southernmost lat (of track)
                            new_record.append(zero) # northernmost lat (of track)
                            new_record.append(zero) # westernmost
                            new_record.append(zero) # easternmost
                            new_record.append(zero) # drogue-off date (Julian day; 0 = drogue not lost, initial value) 
                            new_record.append(sensor_type[0])
                            new_record.append(sensor_type[1])
                            new_record.append(sensor_type[2])
                            new_record.append(sensor_type[3])
                            new_record.append(sensor_type[4])
                            new_record.append(sensor_type[5])
                            new_record.append(zero) # death code (0 = still active/alive, initial value)
                            print(f"{' ' * 6}{new_record}")                           

                            error_message = common.validate_dirfl_record(new_record)
                            if (error_message == None): # Record is valid
                                # Add record.
                                new_records.append(new_record) 
                            else:
                                print("Error: Check " + f"{int(new_record[0])}" + " " + error_message)                           
                    else:
                        print('\n')
                        print(f"{'Error: Check '}{input_file_path}{' format.'}")
                        break
    except OSError as e:
            # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
            # f"Message: {e.strerror}")     = Human-readable OS error string
            # f"Target File: {e.filename}") = Name of the file causing the issue
            message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
            print(message)
    finally:
        if file:
            file.close # Always executes, ensuring the stream is freed

    return new_records

# This routine is used to add a new record to the directory file,
# while creating a timestamped backup copy beforehand.
# It reads info from a previously created file with format:
#    buoy_id, buoy_type, project_number, start_time, start_latitude, start_longitude.
def add_new_record():
    print('\n')
    print(f"{' ' * 9}{'Enter complete file name where info for records are,'}")
    input_file = str(input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/new.lis): '}"))

    print('\n')
    print(f"{' ' * 9}{'Expected file format: id, buoy_type, project_number, start_time, start_latitude, start_longitude.'}")

    # Loads the directory file
    dirfl = DirectoryFile()
    directory_file = dirfl.rdirfl50()

    # Prints a message to the console showing how many rows were successfully loaded.
    print('\n')
    print(f"{'Number of DIR-File records: '}{len(directory_file)}" + '\n')

    new_records = create_new_records_for_directory_file(input_file, directory_file)

    if (len(new_records) > 0):
        # Update the directory file
        for i in range(len(new_records)):
            directory_file.append(new_records[i])
        #print(*directory_file, sep ='\n')
        dirfl.wdirfl50(directory_file)
        added_records = len(new_records)
        print('\n')
        print(f"{'Added records: '}{added_records}" + 
              f"{' ' * 9}{' Original number of records: '}{len(directory_file) - added_records}" +
              f"{' ' * 9}{' New number of records: '}{len(directory_file)}")
    else:
        print('\n')
        print(f"{' ' * 4}" + "No changes")

