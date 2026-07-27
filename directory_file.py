#!/usr/bin/python

# programer: CG July 2026

# Return:
# dirfl - The DIR-File
def rdirfl50():
    # This is acting as the data loader.
    # It opens the binary data DIR-File, reading the data row-by-row
    # and stops automatically when it hits the end of valid data.
    # DIR-File is raw binary (not human-readable text).

    # Import Module
    import struct

    # Defines the chunk size. Because each row has 22 columns 
    # and each number is a 64-bit double (8 bytes), 
    # each line in the file is exactly 176 bytes long.
    CHUNK_SIZE = 22*8
    # Format string:
    # 22d = 22 doubles (176 bytes)
    FORMAT_STRING = '22d'
    # DIR-File path 
    DIRFL_PATH = '/phodnet/drifter/data/files/dirfl50.dat'

    dirfl = []

    try:
        file = None
        # Opens the file for reading binary data.
        with open(DIRFL_PATH, 'rb') as file:
            while True:
                # For large binary files, reading the entire file at once may consume a lot of memory.
                # In such cases, it is better to read the file in smaller chunks using read(size).
                # The file is read in blocks of 176 bytes until no more data is available.
                chunk = file.read(CHUNK_SIZE)
                if not chunk:
                    break
                buoy_id = struct.unpack('d', chunk[:8])[0] # First column

                # If the buoy_id is less than or equal to 0, it means
                # it has reached a blank/sentinel row marking the end
                # of real data.
                if buoy_id > 0:
                    # row example: 
                    # 300534064897810.0, 4401656.0, 2222.0, 48.0, 17201.041015625,
                    # 43.189998626708984, -28.010000228881836, 17261.75, 41.73809814453125, -27.218000411987305,
                    # 41.0, 44.0, -29.0, -27.0, 17201.041015625,
                    # 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0
                    row = struct.unpack(FORMAT_STRING, chunk)
                    dirfl.append(row)
                    
    except OSError as e:
        # f"Error Code: {e.errno}")     = OS error number (e.g., 2 for missing file)
        # f"Message: {e.strerror}")     = Human-readable OS error string
        # f"Target File: {e.filename}") = Name of the file causing the issue
        message = f"Error Code: {e.errno}, " + f"Message: {e.strerror}, " + f"Target File: {e.filename}"
        print(message)
    finally:
        if file:
            file.close # Always executes, ensuring the stream is freed

    return dirfl
