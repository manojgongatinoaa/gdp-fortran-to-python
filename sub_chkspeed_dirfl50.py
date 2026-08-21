#!/usr/bin/python

# Programer CG August 2026

from pathlib import Path

from file_manager import FileManager
from k_file import KFile

SPEED_THRESHOLD = 300.0 # cm/s
FILTER_NINE     = 999

def enter_destination_file():
    print('\n')
    print(f"{' ' * 9}{'Enter output file name,'}")
    return input(f"{' ' * 9}{'(ex. /phodnet/drifter/gonzalez/work/speed.out): '}")

def enter_subset(directory_file):
    start = None
    stop = None
    while True:
        print('\n')
        print(f"{' ' * 9}{'Enter 1,99999 to scan all records in dirfl or'}")
        text = f"{' ' * 9}{'enter start and ending record number in dirfl to scan'}" + '\n'
        answer = input(text)
        spl = answer.split(",")
        if len(spl) > 1:
            start   = int(spl[0])
            stop    = int(spl[1])
            if start == 1 and stop >= 99999:
                # Scan all in directory file.
                stop = len(directory_file)
            if stop >= start:
                break
            print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")

    return start-1, stop-1

def write_file(file_path, my_list):
    overwrite = True
    while True:
        path = Path(file_path)
        # Check if the path exists (can be a file OR a directory)
        if path.exists():
            print('\n')
            answer = input(f"{' ' * 9}{'overwrite '}{file_path}{' ? '}")
            if (answer.strip().upper() == 'Y'):
                overwrite = True
            else:
                overwrite = False
        else:
            overwrite = True

        if overwrite:
            # WRITE FILE
            fl_manager = FileManager()
            fl_manager.write_list('', file_path, my_list)
            break

# Scans the DIR-File, reads each individual K-File, and extracts records where the recorded
# speed exceeds 300 cm/s, writing those anomalous events to an output text file.
# Threshold: 300 cm/s corresponds to 3 m/s (approx. 5.83 knots). The script flags any 
# physical velocity crossing above this ceiling as an anomaly or extreme weather event.
def sub_chkspeed_dirfl50(directory_file):
    # File to write logging summaries.
    file_name = enter_destination_file()
    results = []
    results.append(' The following buoys have speed gt 300 cm/sec')
    # Writes a blank line to the top of the output report file.
    results.append(' ')
    record = ''

    start, stop = enter_subset(directory_file)
    subset = directory_file[start:stop] # Extracts a specific range of rows.

    print('\n' + "Wait!: Verifying speed in the K-File..." + '\n')

    # The 1st column in DIR-File represents the buoy ID.
    for row in subset:
        cnt = 0
        buoy_id = str(int(row[0]))
        kfl     = KFile(buoy_id)
        # row format: time, lat, lon, tmp, ve, vn, spd, v.lat, v.lon, e.tp
        k_file  = kfl.rkfl()
        if len(k_file) > 0:
            # Delete row index 0 permanently, it is a header.
            k_file.pop(0)
            if len(k_file) > 0:
                k_file_300 = [y for y in k_file if y[6] > SPEED_THRESHOLD]
                if len(k_file_300) > 0:
                    for y in k_file_300:
                        # If the speed equals 999 (a common legacy placeholder value
                        # for missing sensor data), it bypasses processing and skips
                        # directly to the next row
                        if int(y[6]) != FILTER_NINE:
                            record = '{:>16}'.format(buoy_id)
                            record += f"{y[0]:10.2f}"
                            record += f"{y[1]:10.2f}"
                            record += f"{y[2]:10.2f}"
                            record += f"{y[4]:10.2f}"
                            record += f"{y[5]:10.2f}"
                            record += f"{y[6]:10.2f}"
                            results.append(record)  
                            cnt =+ 1

        if cnt > 0:
            record = "***************" + '\n'  
            results.append(record)

    write_file(file_name, results)
    print('\n')
    if len(results) > 0:
        text = f"{' file: '}{file_name}{' created with results'}"
    else:
        text = f"{' file: '}{file_name}{' is empty, no discrepancy found'}"
    print(text)
