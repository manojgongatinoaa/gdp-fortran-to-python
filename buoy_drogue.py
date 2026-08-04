#!/usr/bin/python

# Programer: CG July 2026

# Class to safely and easily manage common drogue operations.
class BuoyDrogue:
    def __init__(self, dirfl, gdt):
        self.dirfl = dirfl # The Dir-File
        self.gdt = gdt

    # Retrieve a list of IDs: This function filters and extracts specific oceanographic buoy data
    #                         based on whether the drogue (a sea anchor attached to a buoy) is 
    #                         active lost.
    #
    # Parameters:
    # sel   - The selection flag. Positive values (> 0) look for buoys with drogues on.
    #         Non-positive values (<= 0) look for buoys that lost their drogues.
    #
    # Return:
    #     If buys with drogue on was selected return drogue_on
    #     otherwise return drogue_off
    #     Result list format: buoy_id, experiment_number, buoy_type
    def drogue(self, sel):
        drogue_on = []
        drogue_off = []

        for row in self.dirfl:
            # row example: 
            # 300534064897810.0, 4401656.0, 2222.0, 48.0, 17201.041015625,
            # 43.189998626708984, -28.010000228881836, 17261.75, 41.73809814453125, -27.218000411987305,
            # 41.0, 44.0, -29.0, -27.0, 17201.041015625,
            # 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0

            # The 15th column represents the drogue-off date.
            # If the drogue-off date is less than or equal to 0,
            # it indicates that the drogue was not lost.
            drogue_off_date = row[14]

            # Result list format: buoy_id, experiment_number, buoy_type
            buoy_id = int(row[0])
            experiment_number = int(row[2])
            buoy_type = int(row[3])
            end_date= row[7]
            
            if (sel > 0): # drogue on buoys selected
                if (drogue_off_date <= 0): # drogue still active
                    drogue_on.append([buoy_id, experiment_number, buoy_type])
            else: # drogue off selected
                # If the drogue was lost and the end date is after your cutoff threshold gdt
                if (drogue_off_date > 0 and end_date > self.gdt):
                    drogue_off.append([buoy_id, experiment_number, buoy_type])

        if (sel > 0): # drogue on buoys selected
            return drogue_on
        else: # drogue off buoys selected
            return drogue_off

