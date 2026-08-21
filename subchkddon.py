#!/usr/bin/python

# Programer CG August 2026

import re

from file_manager import FileManager
from common import CommonFunctions

# Checks in DIR-File if a buoy is declared dead and its drogue
# still marked as on.
def subchkddon(directory_file):
    # File to write logging summaries.
    file_name = "chkddon.out"
    results = []
    record = ''

    while True:
        print('\n')
        # Type in the most recent database date representing the latest database update.
        user_input = str(input(f"{' ' * 9}{'Enter last date in database (m/d/y): '}"))        
        common = CommonFunctions()
        if (common.is_valid_date(user_input, "%m/%d/%Y")):
            spl = re.split(r"[/\s -]", user_input)
            if len(spl) > 2:
                year = spl[2]
                month = spl[0]
                day = spl[1]
                header = ' the following buoys are dead but drogue is on' + '\n'
                header += f"{' last update= '}{month}{' '}{day}{' '}{year}{' '}" + '\n'
                results.append(header)
                print('\n')
                print(header)
                
                j_last_date = common.date_to_jd(int(year), int(month), float(day))

                # The 1st column in DIR-File represents the buoy ID.
                # The 3rd column in DIR-File represents the experiment number.
                # The 8th column in DIR-File represents the timestamp of the last successful signal fix.
                # The 15th column in DIR-File represents the drogue-off date.
                # The 22nd column in DIR-File represents the drogue deactivation code.
                for row in directory_file:
                    buoy_id         = int(row[0])
                    exp_no          = int(row[2])
                    end_time        = row[7]
                    drogue_off_date = int(row[14])
                    death_code      = int(row[21])

                    if (death_code > 0 and drogue_off_date == 0):
                        # The buoy's death code is greater than 0 and its drogue status
                        # is still flagged as active/on 
                        date = common.jd_to_date_base(end_time)
                        year = date[0]
                        month = date[1]
                        day = int(date[2])
                        record = f"{'{:>16}'.format(buoy_id)}"
                        record += f"{'{:>6}'.format(exp_no)}"
                        record += f"{'{:>6}'.format(month)}"
                        record += f"{'{:>6}'.format(day)}"
                        record += f"{'{:>6}'.format(year)}"
                        record += f"{'{:>6}'.format(death_code)}"
                        record += f"{'{:>6}'.format(drogue_off_date)}"
                        results.append(record)
                        print(record)

                fl_manager = FileManager()
                fl_manager.write_list('', file_name, results)

                if len(results) > 0:
                    text = f"{' file: '}{file_name}{' created with results'}"
                else:
                    text = f"{' file: '}{file_name}{' is empty, all the dead buoys with drogue off.'}"
                print('\n')
                print(text)

                break
            else:
                print("Error: Check input date")
        else:
            print("Error: Check input date")
