#!/usr/bin/python

# Programer CG August 2026

from file_manager import FileManager

def create_header():
    # Writes a blank line to the top of the output log file.
    header = '\n'
    header += f"{' ' * 12}{'id'}{' ' * 8}{'st'}{' ' * 12}{'et'}{' ' * 10}{'doff'}{' ' * 8}{'diff'}"
    return header

def create_record(row):
    record = '{:>18}'.format(str(int(row[0])))
    record += '{:>12}'.format(str(f"{row[4]:.4f}"))
    record += '{:>12}'.format(str(f"{row[7]:.4f}"))
    record += '{:>12}'.format(str(f"{row[14]:.4f}"))

    return record

# Validates and corrects drogue-off date.
# It ensures that the date the drogue fell off falls logically
# between the deployment start time and end time.
# If drogue-off date is logically impossible, the code automatically
# overwrites it with a valid boundary date.
# Parameter:
#     directory_file - A large 2D matrix DIR-File.
def subchkdro(directory_file):
    # File to write logging summaries.
    file_name = "chkdro.out"
    results = []
    record = ''

    # Initializes the three modification tracking counters to zero.
    # counter number of records with drogue-off date less than start time.
    start_time_cnt  = 0
    # counter number of records with drogue-off date greater than end 
    # for more than one day.
    end_time_cnt    = 0
    # counter number of records which diff (end time - drogue-off date) is less than one day.
    diff_cnt        = 0

    # The 1st column in DIR-File represents the buoy ID.
    # The 5th column in DIR-File represents the deployment timestamp.
    # The 8th column in DIR-File represents the timestamp of the last successful signal fix.
    # The 15th column in DIR-File represents the drogue-off date.
    for row in directory_file:
        # float to exactly 3 decimal places.
        start_time      = round(row[4], 3)
        end_time        = round(row[7], 3)
        drogue_off_time = round(row[14], 3)
    
        # If drogue-off date is equal 0 means drogue still on.
        # If drogue-off date is equal 1 means can't tell status of drogue.
        if (drogue_off_time > 0.0):
            # Is drogue-off date happened before start time?
            if (drogue_off_time < start_time and drogue_off_time > 1.0):
                results.append(create_header())
                # Logs the original faulty record.
                record = f"{create_record(row)}{' ' * 3}{' (doff lt st, changed to st) '}" + '\n'
                # Overwrites the faulty drogue-off time
                row[14] = start_time
                # Logs the newly corrected data.
                record = f"{record}{create_record(row)}{' ' * 3}{' (new record )'}"
                results.append(record)
                # Increments counter tracking adjustments make for early drogue drops.
                start_time_cnt += 1
            else:
                # drogue-off date is validly located on or after the start time.
                # Calculates the operational lifespan duration remaining between the end
                # date and the drogue loss date.
                diff = end_time - drogue_off_time
                # Evaluates if the drogue came off less than 24 hours (1 full day) prior 
                # to the official track end time.
                if (diff > 0.0 and diff < 1.0):
                    results.append(create_header())
                    # Logs the original faulty record.
                    record = create_record(row)
                    record += '{:>12}'.format(str(f"{diff:.4f}"))
                    record = f"{record}{' ' * 3}{' (et-doff lt 1 day,doff=et)'}" + '\n'
                    # Overwrites the faulty drogue-off time
                    row[14] = end_time
                    # Logs the newly corrected data.
                    record += create_record(row)
                    record += '{:>12}'.format(str(f"{diff:.4f}"))
                    record = f"{record}{' ' * 3}{' (new record)'}"
                    results.append(record)
                    # Increments the count tracker for records modified due to 
                    # the sub-24-hour buffer constraint.
                    diff_cnt += 1
                else:
                    if (diff < 0.0):
                        # Handles physical impossibilities where the drogue-off date occurs
                        # after end time.
                        results.append(create_header())
                        # Logs the original faulty record.
                        record = create_record(row)
                        record += '{:>12}'.format(str(f"{diff:.4f}"))
                        record = f"{record}{' ' * 3}{' (doff gt et, doff=et)'}" + '\n'
                        # Overwrites the faulty drogue-off time
                        row[14] = end_time
                        # Logs the newly corrected data.
                        record += create_record(row)
                        record += '{:>12}'.format(str(f"{diff:.4f}"))
                        record = f"{record}{' ' * 3}{' (new rec)'}"
                        results.append(record)
                        # Increments the tracking counter for instances where drogue-off date
                        # exceeded the end time.
                        end_time_cnt += 1
                
    # Appends the sum totals of all updates made to the bottom of chkdro.out log file.
    bottom = '\n' + f"{' # rec fixed: dof let st= '}{' ' * 12}{start_time_cnt}" + '\n'
    bottom = bottom + f"{' # rec fixed: doff lt 2 days et= '}{' ' * 12}{diff_cnt}" + '\n'
    bottom = bottom + f"{' # rec fixed: doff gt et= '}{' ' * 12}{end_time_cnt}" + '\n' 
    results.append(bottom)

    fl_manager = FileManager()
    fl_manager.write_list('', file_name, results)
    if len(results) > 0:
        text = f"{' file: '}{file_name}{' created with results'}"
    else:
        text = f"{' file: '}{file_name}{' is empty, drogue-off date is OK'}"
    print(text)

    return directory_file