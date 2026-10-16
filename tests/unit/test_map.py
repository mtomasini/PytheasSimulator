import pandas as pd
from pytheas_simulator.map import Map


def test_load_map_data():
    # WORKED FINE. CHANGED NAME OF TEST TO AVOID AUTOMATIC TEST INTEGRATION
    WIND_DATA = "./tutorial/data/environmental_data/winds/"
    CURRENT_DATA = "./tutorial/data/environmental_data/currents/"
    WAVES_DATA = "./tutorial/data/environmental_data/waves/"
    
    bounding_box = [56.3, 5.8, 58.8, 13.1] # bounding_box for the Skagerrak strait
    testing_map = Map(bounding_box = bounding_box, 
                      earliest_time = '1996-07-01',
                      latest_time = '1996-07-31',
                      wind_data_path=WIND_DATA,
                      current_data_path=CURRENT_DATA,
                      waves_data_path=WAVES_DATA)
    
    assert testing_map.winds_data.latitude.max() > bounding_box[2]
    assert testing_map.currents_data.time.max() < pd.Timestamp('1996-08-01')
    assert testing_map.waves_data.time.min() > pd.Timestamp('1995-11-21')
    
    assert testing_map.return_local_winds([57.7, 9], pd.Timestamp('1996-07-31')) is not None
    assert testing_map.return_local_currents([57.7, 9], pd.Timestamp('1996-07-05')) is not None
    assert testing_map.return_local_waves([57.7, 9], pd.Timestamp('1995-12-31')) is None
    
    
def test_find_closest_land():
    # WORKED FINE. CHANGED NAME OF TEST TO AVOID AUTOMATIC TEST INTEGRATION
    WIND_DATA = "./tutorial/data/environmental_data/winds/"
    CURRENT_DATA = "./tutorial/data/environmental_data/currents/"
    WAVES_DATA = "./tutorial/data/environmental_data/waves/"
    
    bounding_box = [56.3, 5.8, 58.8, 13.1] # bounding_box for the Skagerrak strait
    testing_map = Map(bounding_box = bounding_box, 
                      earliest_time = '1996-07-14',
                      latest_time = '1996-07-15',
                      wind_data_path=WIND_DATA,
                      current_data_path=CURRENT_DATA,
                      waves_data_path=WAVES_DATA)
    
    distance, angle = testing_map.find_closest_land([58.0, 11.5])
    assert angle < 180
    assert distance < 10