#!/usr/bin/python

# Programer CG August 2026

from database_manager import DatabaseManager
from file_manager import FileManager
from deployed_log import DeployedLog

# Read the DIR-File to find buoys that has the WMO number equal 0.
# Then it will look in the IMEI_LUT.dat file and if that ID has a 
# WMO number currently assigned, it will write it in the DIR-File.  
# It optionally wrties a new DIR-File or just produces the listing
# file chkwmo.out
def subchkwmo(directory_file):
    # File to write logging summaries.
    file_name = "chkwmo.out"
    results = []
    header = ' the following ids had no wmo assigned in dirfl' + '\n\n'
    header += f"{' ' * 4}{'id'}{' ' * 6}{'wmo'}" + '\n\n'
    results.append(header)
    record = ''
    # The total number of valid active buoy into the DIR-File.
    cnt = 0

    where = ''
    db_manager = DatabaseManager()
    # The 1st column in DIR-File represents the buoy ID.
    # The 2nd column in DIR-File represents the WMO number.
    for row in directory_file:
        buoy_id = str(int(row[0]))
        wmo_no  = int(row[1])
        # If a valid WMO exists, it skips everything and proceeds 
        # immediately to the next buoy.
        if (wmo_no == 0):
            # WMO number doesn't exist in DIR-File.
            print('\n')
            print(f"{'{:>20}'.format(buoy_id)}{'{:>12}'.format(str(wmo_no))}")
            print(' looking in IMEI_LUT.dat')
            # Get WMO number and put in DIR-File if it is found.
            wmo_no = int(db_manager.select_wmo(buoy_id))
            if wmo_no != 0:
                where = ' found in IMEI_LUT.dat' + '\n'
            else:
                print(' not found in IMEI_LUT.dat')
                print(' looking in deployed.log')
                # add WMO number from deployed.log file.
                deployed_log = DeployedLog()
                wmo_no = int(deployed_log.get_wmo(buoy_id))
                if wmo_no != 0:
                    where = ' found in deployed.log' + '\n'
                else:
                   print(' not found in deployed.log') 

            if wmo_no != 0:
                row[1] = float(wmo_no)
                print(f"{'{:>20}'.format(buoy_id)}{'{:>12}'.format(str(wmo_no))}")
                record = f"{'{:>16}'.format(buoy_id)}{'{:>8}'.format(str(wmo_no))}"
                record += where
                results.append(record)

    fl_manager = FileManager()
    fl_manager.write_list('', file_name, results)

    if len(results) > 0:
        text = f"{' file: '}{file_name}{' created with results'}"
    else:
        text = f"{' file: '}{file_name}{' is empty, all WMO number are currently assigned'}"
    print('\n')
    print(text)

    return directory_file