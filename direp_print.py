#!/usr/bin/python

# Programer CG August 2026

from common import CommonFunctions

def create_record(row, jd_to_date):
    if len(row) > 21:
        # The 1st column in DIR-File represents the buoy ID.
        # The 2nd column in DIR-File represents the WMO number.
        # The 3rd column in DIR-File represents the experiment  number.
        # The 4th column in DIR-File represents the buoy type classification code.
        # The 5th column in DIR-File represents the deployment timestamp.
        # The 6th column in DIR-File represents the deployment latitude coordinate.
        # The 7th column in DIR-File represents the deployment longitude coordinate.
        # The 8th column in DIR-File represents the timestamp of the last successful signal fix.
        # The 9th column in DIR-File represents the last recorded latitude coordinate.
        # The 10th column in DIR-File represents the last recorded longitude coordinate.
        # The 15th column in DIR-File represents the drogue-off date.
        # From 16th column to 21st column in DIR-File represents the instrument sensor status flags.
        # The 22th column in DIR-File represents the death code.

        # Longitude Normalization:
        # Longitude is stored in DIR-File as - for east, + west
        lon = row[6] # deployment longitude
        if lon < 0.0: # originally East
            # Example: If a position is 45°E, it is stored as -45.0.
            # Multiplying by -1.0 yields 45.0°E.
            lon = lon * -1.0
        else: # originally West
            # Example: If a position is 90°W, it is stored as +90.0.
            # Evaluating 360.0 - 90.0 converts it into 270.0°E heading
            # eastward around the globe.
            lon = 360.0 - lon
        row[6] = lon # last recorded longitude
        lon = row[9]
        if lon < 0.0:
            lon = lon * -1.0 # stored in dir as - for east, + west
        else:
            lon = 360.0 - lon
        row[9] = lon

        start_time      = str(f"{row[4]:.3f}")
        end_time        = str(f"{row[7]:.3f}")
        drogue_off_time = str(f"{row[14]:.3f}")

        # Switch formatting based on whether you want standard
        # calendar dates (Month/Day/Year) or Julian days.
        if (jd_to_date):
            common = CommonFunctions()
            # Convert Julian Day to date.
            date = common.jd_to_date_base(row[4])
            # Format into a "MM DD.DD YYYY" string format
            start_time = common.format_date(date)

            if (row[7] > 0.0): # If ending date greater than 0, convert.
                # Only if buoy was killed, convert the date.
                # Convert Julian Day to date.
                date = common.jd_to_date_base(row[7])
                # Format into a "MM DD.DD YYYY" string format
                end_time = common.format_date(date)
            else:
                end_time = '0 0.0 0000'

            if (row[14] > 0.0): # If drogue-off date greater than 0, convert.
                # Only if drogue was lost
                # Convert Julian Day to date.
                date = common.jd_to_date_base(row[14])
                # Format into a "MM DD.DD YYYY" string format
                drogue_off_time = common.format_date(date)
            else:
                drogue_off_time = '0 0.0 0000'
        
        record = '{:>15}'.format(str(int(row[0])))
        record += '{:>9}'.format(str(int(row[1])))
        record += '{:>6}'.format(str(int(row[2])))
        record += '{:>3}'.format(str(int(row[3])))
        record += '{:>14}'.format(start_time)
        record += '{:>8}'.format(str(f"{row[5]:.3f}"))
        record += '{:>9}'.format(str(f"{row[6]:.3f}"))
        record += '{:>14}'.format(end_time)
        record += '{:>8}'.format(str(f"{row[8]:.3f}"))
        record += '{:>9}'.format(str(f"{row[9]:.3f}"))
        record += '{:>14}'.format(drogue_off_time)
        record += '{:>2}'.format(str(int(row[15])))
        record += '{:>2}'.format(str(int(row[16])))
        record +=.format(str(int(row[17])))
        record += '{:>2}'.format(str(int(row[18])))
        record = record + '{:>2}'.format(str(int(row[19])))
        record = record + '{:>2}'.format(str(int(row[20])))
        record = record + '{:>2}'.format(str(int(row[21])))
    
    return record

def header_julian_date() -> str:
    # prints julian date
    header3 = f"{'b':>25}{'dep':>6}{'dep':>9}{'dep':>8}"
    header3 += f"{'end':>5}{'end':>8}{'end':>7}"
    header3 += f"{'drog':>8}{'sensors':>9}{'type':>7}" + '\n'

    header4 = f"{'id':>9}{'wmo':>6}{'exp':>6}"
    header4 += f"{'ty':>4}{'time':>7}{'lat':>8}"
    header4 += f"{'lon':>8}{'time':>6}{'lat':>7}"
    header4 += f"{'lon':>7}{'lost':>8}{'death':>17}" + '\n\n'
    
    return header3 + header4
    
def header_date() -> str:
    # prints m d y
    header3 = f"{'b':>25}{'dep. time':>12}{'dep':>9}"
    header3 += f"{'dep':>7}{'end time':>13}{'end':>9}"
    header3 += f"{'end':>7}{'drog lost':>14}{'sensors':>13}"
    header3 += f"{'type':>7}" + '\n'

    header4 = f"{'id':>9}{'wmo':>6}{'exp':>6}"
    header4 += f"{'ty':>4}{'m':>4}{'d':>4}"
    header4 += f"{'y':>4}{'lat':>9}{'lon':>7}"
    header4 += f"{'m':>5}{'d':>4}{'y':>4}"
    header4 += f"{'lat':>8}{'lon':>7}{'m':>7}"
    header4 += f"{'d':>4}{'y':>4}{'death':>20}" + '\n'
    
    return header3 + header4

def create_header(exp_no, text, jd_to_date):
    header1 = '\n'
    header1 += '{:>2}'.format('*** e x p e r i m e n t  ')
    header1 += '{:>1}'.format(str(exp_no)) + '{:>1}'.format("  b u o y s ***")
    header1 += '\n\n\n'
    
    header2 = f"{'{:>2}'.format('***** ')}{text}{'   b u o y s *****'}"
    header2 += '\n\n'
    
    header_3_4 = ""
    if not jd_to_date:
        header_3_4 = header_julian_date()
    else:
        header_3_4 = header_date()

    return header1 + header2 + header_3_4

# *********************************
# *** list by experiment number ***
# *********************************

# This function formats and writes records from DIR-File like buoy id,
# WMO number, experiment number, buoy type, etc) to a specified text file
# listing all active buoys by experiment number.
# It switches formatting based on whether you want standard calendar dates
# (Month/Day/Year) or Julian days.
def dprint_active_by_experiment(exp_no, directory_file, jd_to_date):  
    file_for05X = []
    # Start with the header.
    file_for05X.append(create_header(exp_no, "a c t i v e", jd_to_date))
    
    # Formats and creates records
    for row in directory_file:
        if (len(row) > 21):
            # Checks if this buoy's experiment column matches.
            if (int(exp_no) == int(row[2]) and
                int(row[21] == 0)): # shows only active buoys.
                file_for05X.append(create_record(row, jd_to_date))

    return file_for05X
    
# This function formats and writes records from DIR-File like buoy id,
# WMO number, experiment number, buoy type, etc) to a specified text file
# listing all dead buoys by experiment number.
# It switches formatting based on whether you want standard calendar dates
# (Month/Day/Year) or Julian days.
def dprint_dead_by_experiment(exp_no, directory_file, jd_to_date):
    file_for05X = []
    # Start with the header.
    file_for05X.append(create_header(exp_no, "d e a d", jd_to_date))
    
    # Formats and creates records
    for row in directory_file:
        if (len(row) > 21):
            # Checks if this buoy's experiment column matches.
            if (int(exp_no) == int(row[2]) and
                int(row[21] != 0)): # shows only dead buoys.
                file_for05X.append(create_record(row, jd_to_date))
        
    return file_for05X
    
# This function formats and writes records from DIR-File like buoy id,
# WMO number, experiment number, buoy type, etc) to a specified text file
# listing all buoys by experiment number.
# It switches formatting based on whether you want standard calendar dates
# (Month/Day/Year) or Julian days.
def dprint_all_by_experiment(exp_no, directory_file, jd_to_date):
    file_for05X = []
    # Start with the header.
    file_for05X.append(create_header(exp_no, " a l l", jd_to_date))
    
    # Formats and creates records
    for row in directory_file:
        if (len(row) > 21):
            # Checks if this buoy's experiment column matches.
            if (int(exp_no) == int(row[2])): # shows all buoys buoys.
                file_for05X.append(create_record(row, jd_to_date))

    return file_for05X

# ******************************************************
# *** list all buoys regardless of experiment number ***
# ******************************************************

# This function formats and writes records from DIR-File like buoy id,
# WMO number, experiment number, buoy type, etc) to a specified text file
# listing all active buoys.
# It switches formatting based on whether you want standard calendar dates
# (Month/Day/Year) or Julian days.
def dprint_active(directory_file, jd_to_date):  
    file_for05X = []
    # Start with the header.
    file_for05X.append(create_header('', "a c t i v e", jd_to_date))
    
    # Formats and creates records
    for row in directory_file:
        if (len(row) > 21):
            if (int(row[21] == 0)): # shows only active buoys.
                file_for05X.append(create_record(row, jd_to_date))

    return file_for05X
    
# This function formats and writes records from DIR-File like buoy id,
# WMO number, experiment number, buoy type, etc) to a specified text file
# listing all dead buoys.
# It switches formatting based on whether you want standard calendar dates
# (Month/Day/Year) or Julian days.
def dprint_dead(directory_file, jd_to_date):
    file_for05X = []
    # Start with the header.
    file_for05X.append(create_header('', "d e a d", jd_to_date))
    
    # Formats and creates records
    for row in directory_file:
        if (len(row) > 21):
            if (int(row[21] != 0)): # shows only dead buoys.
                file_for05X.append(create_record(row, jd_to_date))
        
    return file_for05X
    
# This function formats and writes records from DIR-File like buoy id,
# WMO number, experiment number, buoy type, etc) to a specified text file
# listing all buoys.
# It switches formatting based on whether you want standard calendar dates
# (Month/Day/Year) or Julian days.
def dprint_all(directory_file, jd_to_date):
    file_for05X = []
    # Start with the header.
    file_for05X.append(create_header('', " a l l", jd_to_date))
    
    # Formats and creates records
    for row in directory_file:
        if (len(row) > 21):
            # shows all buoys buoys.
            file_for05X.append(create_record(row, jd_to_date))

    return file_for05X

