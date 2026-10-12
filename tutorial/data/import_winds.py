"""
This script imports winds data in the format necessary to run Pytheas Simulator.

You can change parameters to modify the import according to your needs. The variables collected by this scripts are
the wind direction and speed at 10m above the surface for the year 2025, for the area covered in the article. 
"""

import cdsapi

months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

for month in months:

    dataset = "reanalysis-cerra-single-levels"
    request = {
        "variable": [
            "10m_wind_direction",
            "10m_wind_speed"
        ],
        "level_type": "surface_or_atmosphere",
        "data_type": ["reanalysis"],
        "product_type": "analysis",
        "year": ["2025"],
        "month": [
            f"{month}"
        ],
        "day": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28", "29", "30",
            "31"
        ],
        "time": [
            "00:00", "06:00",
            "12:00", "18:00"
        ],
        "data_format": "netcdf"

    }

    client = cdsapi.Client()
    target = f"./data/environmental_data/winds/2025/month_{month}.nc"
    client.retrieve(dataset, request, target).download()