#!/usr/bin/python

# Programer CG August 2026

from constants import data_type_directory
from constants import data_type_prefix

def get_file_prefix(file_type):
    result = ''

    if file_type <= 1 and file_type <= 4:
        result = data_type_prefix[file_type]

    return result

def get_directory_path (file_type):
    result = ''

    if file_type <= 1 and file_type <= 4:
        result = data_type_directory[file_type]

    return result

# This will find the directory and file name given a buoy ID and data type.
# Parameters:
#    buoy_id        - Unique buoy identification number.
#    file_type      - data type (1: Raw, 2: Acc Edi/Pos, 3: Ac Edit Sensor, 4: Krigged).
# Return:
#    file_name      - Generated file name.
#    directory_path - Generated directory path.
def dfname15(buoy_id: int, file_type: int):
    # Get the single-letter prefix based on the data type.
    prefix = get_file_prefix(file_type)
    file_name = f"{prefix}{str(buoy_id)}"
    directory_path = get_directory_path(file_type)

    return file_name, directory_path

    