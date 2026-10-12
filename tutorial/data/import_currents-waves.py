"""
This script imports currents and waves data in the format necessary to run Pytheas Simulator.

You can change parameters to modify the import according to your needs. The variables collected by this scripts are
the wind direction and speed at 10m above the surface for the year 2025, for the area covered in the article. 
"""

import copernicusmarine


def monthly_import(dataset, type_of_dataset):
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    if type_of_dataset == "currents":
        # ATTENTION! there are datasets out there that call currents in the x and y component "uo" and "vo" instead!
        variables = ["vxo", "vyo"]
    elif type_of_dataset == "waves":
        variables = ["VHM0"]

    for month in months:
        last_day = "31" 
        if month in ["04", "06", "09", "11"]: 
            last_day = "30"
        elif month == "02":
            # here we are downloading for 2025, but in case of a leap year this should be "29"!
            last_day = "28"
        
        copernicusmarine.subset(
            dataset_id = dataset,
            variables = variables,
            minimum_longitude = -29.720039021480375,
            maximum_longitude = 10.480836622997344,
            minimum_latitude = 55.8011102398125,
            maximum_latitude = 65.84004107063826,
            start_datetime = f"1995-{month}-01T00:00:00",
            end_datetime = f"1995-{month}-{last_day}T23:59:59",
            minimum_depth = 0,
            maximum_depth = 0,
            output_filename = f"month_{month}.nc",
            output_directory = f"./data/environmental_data/{type_of_dataset}/"
    )

monthly_import("cmems_mod_arc_phy_my_topaz4_P1D-m", "currents")
monthly_import("cmems_mod_arc_wav_my_3km-climatology_P1M-m", "waves")