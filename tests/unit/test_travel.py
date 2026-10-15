import numpy as np
import pandas as pd
from pytheas_simulator import boat, map, travel

def test_travel_step():
    WIND_DATA = "./tutorial/data/environmental_data/winds/"
    CURRENT_DATA = "./tutorial/data/environmental_data/currents/"
    WAVES_DATA = "./tutorial/data/environmental_data/waves/"
    SPEED_POLAR_DIAGRAM_PATH = './polar_diagrams/hjortspring_speeds_16pad_3000kg_44cad_75oars_2oars.csv'
    LEEWAY_POLAR_DIAGRAM_PATH = './polar_diagrams/hjortspring_leeway_empty_diagram.csv'
    speed_polar_diagram = pd.read_csv(SPEED_POLAR_DIAGRAM_PATH, sep=",", index_col=0)
    leeway_polar_diagram = pd.read_csv(LEEWAY_POLAR_DIAGRAM_PATH, sep=",", index_col=0)
    bounding_box = [56.3, 5.8, 58.8, 13.1] # bounding_box for the Skagerrak strait

    testing_map = map.Map(bounding_box = bounding_box, 
                          earliest_time = '1996-07-01',
                          latest_time = '1996-07-31',
                          wind_data_path=WIND_DATA,
                          current_data_path=CURRENT_DATA,
                          waves_data_path=WAVES_DATA)

    departure_site = testing_map.find_closest_water([57.5, 11.5]) # departure should already be in the middle of water

    test_boat = boat.Boat(craft = "I have been tested",
                          latitude = departure_site[0],
                          longitude = departure_site[1],
                          speed_polar_diagram=speed_polar_diagram,
                          leeway_polar_diagram=leeway_polar_diagram,
                          target = [57.7, 11.2])

    test_travel = travel.Travel(boat = test_boat, 
                                map = testing_map, 
                                start_day = "1996-07-05", 
                                timestep = 15,
                                max_duration = 24, 
                                night_travel = False, 
                                twilights_of_stops = 'astronomical')

    # test_travel.step()

    test_travel.run()

    assert test_boat.latitude != departure_site[0]
    assert test_boat.longitude != departure_site[1]

    assert len(test_boat.trajectory) > 10
    assert test_boat.latitude < 57.7 # vessel comes from below, so it should not exceed target
    assert test_boat.latitude > 11 # vessel should not have strayed so much West


def test_travel_route():
    WIND_DATA = "./tutorial/data/environmental_data/winds/"
    CURRENT_DATA = "./tutorial/data/environmental_data/currents/"
    WAVES_DATA = "./tutorial/data/environmental_data/waves/"
    SPEED_POLAR_DIAGRAM_PATH = './polar_diagrams/hjortspring_speeds_16pad_3000kg_44cad_75oars_2oars.csv'
    LEEWAY_POLAR_DIAGRAM_PATH = './polar_diagrams/hjortspring_leeway_empty_diagram.csv'
    speed_polar_diagram = pd.read_csv(SPEED_POLAR_DIAGRAM_PATH, sep=",", index_col=0)
    leeway_polar_diagram = pd.read_csv(LEEWAY_POLAR_DIAGRAM_PATH, sep=",", index_col=0)
    bounding_box = [56.3, 5.8, 58.8, 13.1] # bounding_box for the Skagerrak strait
    
    testing_map = map.Map(bounding_box = bounding_box, 
                          earliest_time = '1996-07-01',
                          latest_time = '1996-07-31',
                          wind_data_path=WIND_DATA,
                          current_data_path=CURRENT_DATA,
                          waves_data_path=WAVES_DATA)
    
    departure_site = testing_map.find_closest_water([57.7, 11.6])
    landing_site = testing_map.find_closest_water([59, 19.79])
    
    route = [[57.7, 11.4], 
            [58.0, 11.1],
            [58.2, 10.9],
            [58.4, 10.4]]

    route = testing_map.create_route(departure_site, landing_site, 
                                     target_interval = 2, 
                                     weights = [1, 1000, 1, 1000], 
                                     iterations = [10, 5, 3, 1])
    
    test_boat = boat.Boat(craft = "I have been tested",
                              latitude = departure_site[0],
                              longitude = departure_site[1],
                              speed_polar_diagram=speed_polar_diagram,
                              leeway_polar_diagram=leeway_polar_diagram,
                              route_to_take = route,
                              target = [landing_site[0], landing_site[1]])
    
    test_travel = travel.Travel(boat = test_boat, 
                                map = testing_map, 
                                start_day = "1996-07-05", 
                                timestep = 15,
                                max_duration = 72, 
                                night_travel = True, 
                                twilights_of_stops = 'nautical')
    
    test_travel.step()
    
    assert test_boat.latitude != departure_site[0]
    assert test_boat.longitude != departure_site[1]