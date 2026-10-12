#### IMPORTANT: THIS SCRIPT IS NOT YET WORKING. ####
# I will work on it in the coming days.

import gc
import numpy as np
import pandas as pd
from pathlib import Path
import sys
import time

from pytheas.boat import Boat
from pytheas.map import Map
from pytheas.travel import Travel
from pytheas.utilities import calculate_start_of_day
from parameters import *
# initiate parameters
speed_polar_diagram = pd.read_csv(SPEED_POLAR_DIAGRAM_PATH, sep=",", index_col=0)
leeway_polar_diagram = pd.read_csv(LEEWAY_POLAR_DIAGRAM_PATH, sep=",", index_col=0)

day_frequency = 3

if len(sys.argv) == 7:
    type_of_trip = sys.argv[1]
    launching_site = locations[sys.argv[2]]
    landing_site = locations[sys.argv[3]]
    start_year = int(sys.argv[4])
    end_year = int(sys.argv[5])
    output = sys.argv[6]
    frequency = day_frequency
elif len(sys.argv) == 5:
    type_of_trip = sys.argv[1]
    launching_site = locations[sys.argv[2]]
    landing_site = locations[sys.argv[3]]
    start_year = 1993
    end_year = 2020
    output = sys.argv[4]
    frequency = day_frequency
elif len(sys.argv) == 1: # FOR TESTING
    type_of_trip = "coastal"
    travel_by_night = True
    launching_site = locations["COPENHAGEN"]
    landing_site = locations["KALMAR"]
    start_year = 1995
    end_year = 1995
    output = "Test"
    frequency = 300
else:
    raise NameError(f"You input only {len(sys.argv) - 1} parameters! At least 4 parameters are needed.")

Path(f"/run/media/mtomasini/LaCie/LIR/Baltic_Experiments/Outputs/{output}").mkdir(parents=True, exist_ok=True)

bounding_box = bounding_box_from_points(launching_site, landing_site, buffer=3)

# frequency = 403 # days
max_duration_h = 1080

last_possible_day = '12-01' # 31 Dec minus max_duration in days / TODO write function for this

years = range(start_year, end_year + 1)

if output != "Test":
    if output.split('-')[-1] == "crossing":
        travel_by_night = False
    else:
        travel_by_night = True


for year in years:
    first_simulated_day = '01-02' if year==1993 else '01-01'
    # simulate days from January to 31st of December (accounting for max 72 hours, but after 20200 trips on Dec 30th and 31st cannot be completed in 72 hours due to lack of data after 2020)
    last_simulated_day = last_possible_day if year==2020 else '12-31' 
    dates_to_simulate = pd.date_range(f"{year}-{first_simulated_day}", f"{year}-{last_simulated_day}", freq=f"{frequency}D")

    start_time = time.time()

    earliest_data_time = pd.Timestamp(f"{year}-{first_simulated_day}T01:00")
    latest_data_time = dates_to_simulate[-1] + pd.Timedelta(max_duration_h, "hours")

    # initiate map once for the year
    travel_map = Map(bounding_box, earliest_time=earliest_data_time, latest_time=latest_data_time, 
                        wind_data_path = WIND_DATA, current_data_path=CURRENT_DATA, waves_data_path=WAVES_DATA)
    launching_site_water = travel_map.find_closest_water(launching_site)
    landing_site_water = travel_map.find_closest_water(landing_site)

    # create route
    if type_of_trip == 'coastal':
        try: 
            route = np.loadtxt(f'./Routes/{output}.csv', delimiter=",")
            route = route.tolist()
            # route = list(reversed(route)) 
        except:
            route = travel_map.create_route(launching_site_water, landing_site_water, target_interval = 2, weights = [1, 1000, 1, 1000], iterations = [10, 5, 3, 1])

    else: 
        route = None
    

    for day in dates_to_simulate:
        start_day = pd.Timestamp(day) # calculate_start_of_day(day, launching_site, type_of_twilight='civil') #pd.Timestamp('1995-03-03')
        
        # calculate maximal end day after 72 + 1 hours of navigation
        end_day = calculate_start_of_day(day, launching_site, type_of_twilight='civil') + pd.Timedelta(max_duration_h, unit="hours")

    
        # find closest water point to launching site
        launching_site_water = travel_map.find_closest_water(launching_site)

        # initiate boat
        hjortspring = Boat(hjortspring = Boat('Hjortspring', latitude=launching_site_water[0], longitude=launching_site_water[1],
                           target=landing_site, land_radar_on=True, speed_polar_diagram=speed_polar_diagram, 
                           leeway_polar_diagram=leeway_polar_diagram, route_to_take = route))

        # initiate travel
        travel = Travel(boat = hjortspring, map = travel_map, start_day = start_day, 
                        max_duration = max_duration_h, timestep = 15, night_travel=travel_by_night, 
                        twilights_of_stops='civil', tolerance_distance_landing=5, tolerance_distance_targets=1)
        travel.run(verbose=True)

        travel.output_geojson(f"/run/media/mtomasini/LaCie/LIR/Baltic_Experiments/Outputs/{output}/{day.strftime('%Y-%m-%d')}") # ("./Outputs/test_trajectory") # 
        travel.append_to_aggregates(f"/run/media/mtomasini/LaCie/LIR/Baltic_Experiments/Aggregates/{output}.csv", radius_for_success=10)

    
    del travel_map
    gc.collect()

    if output == "Test":
        if type_of_trip == 'coastal':
            hjortspring.plot_trajectory(bounding_box, show_route=True)
        else:
            hjortspring.plot_trajectory(bounding_box)

    end_time = time.time()
    print(f"Simulation of year {year} completed in about {round((end_time-start_time)/60, 2)} minutes.")