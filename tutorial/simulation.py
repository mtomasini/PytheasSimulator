"""
This script contains a typical simulation script for a set of dates. More complex scripts can be requested for large sets of simulations making use monthly loops over multiple 
years and so fort, but they also require a lot of data to function!
"""

import numpy as np
import pandas as pd
from pathlib import Path
import time

from pytheas_simulator.boat import Boat
from pytheas_simulator.map import Map
from pytheas_simulator.travel import Travel
from pytheas_simulator.utilities import calculate_start_of_day, bounding_box_from_points

# initiate parameters

experiment_name = "script_experiment_gothenburg-tanum"

speed_polar_diagram = pd.read_csv("../polar_diagrams/hjortspring_speeds_16pad_3000kg_44cad_75oars_2oars.csv", sep=",", index_col=0)
leeway_polar_diagram = pd.read_csv("../polar_diagrams/hjortspring_leeway_empty_diagram.csv", sep=",", index_col=0)

WIND_DATA = "./data/environmental_data/winds/"
CURRENT_DATA = "./data/environmental_data/currents/"
WAVES_DATA = "./data/environmental_data/waves/"

locations = {
    "GOTHENBURG" : [57.66, 11.72],
    "SKAGEN" : [57.72, 10.61],
    "TANUM" : [58.70, 11.16]
}

launching_site = locations["GOTHENBURG"]
landing_site = locations["TANUM"]

# this snippet creates a folder if it does not exist with the name of the experiment chosen before
Path(f"./simulation_output/Outputs/{experiment_name}").mkdir(parents=True, exist_ok=True)   

bounding_box = bounding_box_from_points(launching_site, landing_site, buffer=1)

dates_to_simulate = ["1996-07-05", "1996-07-10", "1996-07-15"]
max_duration_in_hours = 288 # 12 days

starting_time = time.time()
travel_map = Map(bounding_box, earliest_time="1996-07-01", latest_time="1996-07-31", 
                 wind_data_path = WIND_DATA, current_data_path=CURRENT_DATA, waves_data_path=WAVES_DATA)
print(f"Map generated in {round((time.time()-starting_time)/60, 2)} minutes.")

launching_site_water = travel_map.find_closest_water(launching_site)
landing_site_water = travel_map.find_closest_water(landing_site)

# if you wet through the vignette before, it should find the route in your folders. Otherwise, it will calculate it from scratch:
try: 
    route = np.loadtxt(f'./routes/gothenburg_tanum.csv', delimiter=",")
    route = route.tolist()
except:
    route = travel_map.create_route(launching_site_water, landing_site_water, target_interval = 2, weights = [1, 1000, 1, 1000], iterations = [10, 5, 3, 1])    

for day in dates_to_simulate:
    time_now = time.time()
    start_day = pd.Timestamp(day) # calculate_start_of_day(day, launching_site, type_of_twilight='civil') #pd.Timestamp('1995-03-03')
        
    # calculate maximal end day after 10 days of navigation
    end_day = calculate_start_of_day(day, launching_site, type_of_twilight='civil') + pd.Timedelta(max_duration_in_hours, unit="hours")


        # initiate boat
    hjortspring = Boat('Hjortspring', latitude=launching_site_water[0], longitude=launching_site_water[1],
                       target=landing_site, land_radar_on=True, speed_polar_diagram=speed_polar_diagram, 
                       leeway_polar_diagram=leeway_polar_diagram, route_to_take = route)

    # initiate travel
    travel = Travel(boat = hjortspring, map = travel_map, start_day = start_day, 
                    max_duration = max_duration_in_hours, timestep = 15, night_travel=True, 
                    twilights_of_stops='civil', tolerance_distance=2)
    travel.run(verbose=True)

    travel.output_geojson(f"./simulation_output/Outputs/{experiment_name}/{day}")  
    travel.append_to_aggregates(f"./simulation_output/Aggregates/{experiment_name}.csv", radius_for_success=5)

    end_time = time.time()
    print(f"Simulation of date {day} completed in about {round((end_time-end_time)/60, 2)} minutes.")

    # Uncomment this line if you want to visualize the voyage at every simulated day (but remember to close the plot window when it pops out, or it will hang the simulation!)
    # hjortspring.plot_trajectory(bounding_box, show_route=True)