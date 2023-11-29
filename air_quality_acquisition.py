# air_quality_acquisition.py
# This is a script that allows user to run a .py function to acquire information about various locations given that they provide a 
# location name and latitude and longitude and there is a given monitor near that location
# 
# By Group 9 (Michael Algarra, Winn Constantini, Shawn Oyer)

import requests
import pandas as pd
import functools as ft
import os
from tkinter.filedialog import askdirectory

# in order to ignore the unverified certificate warning when pulling from web api's
import warnings
warnings.filterwarnings("ignore")

# set default locations for use
city_dicts = {
    "Los Angeles": {
        "lat": '34.114789', 
        "long": "-118.259486"
        }, 
    "Seattle":{
        "lat": "47.613570",
        "long": "-122.347233"
    }
}

def get_ejscreen_df(lat:str,lon:str,buffer:str):
    """Pulls from EJ Screen API for specific latitudes, longitudes, and a specific buffer

    Args:
        lat (str): latitude
        lon (str): longitude
        buffer (str): Buffer for the pull

    Returns:
        pd.DataFrame: a DataFrame with EJ Screen data
    """    
    #api call
    print(f"Pulling EJ Screen data for: latitude: {lat}, and longitude: {lon}")
    url = 'https://ejscreen.epa.gov/mapper/ejscreenRESTbroker1.aspx?namestr=&geometry={"spatialReference":{"wkid":4326},"x":' + lon + ',"y":' + lat + ' }&distance=' + buffer + '&unit=9035&areatype=&areaid=&f=json'
    response = requests.get(url,verify=False)
    r_dict = response.json()

    #dicts to one row dataframes
    
    #get demographics columns into separate dict and then a dataframe
    dem_dict = r_dict['data']['demographics']
    df_dem = pd.DataFrame(dem_dict, index=[0])
    df_dem = df_dem[['P_LOWINC','PCT_MINORITY', 'P_EDU_LTHS','P_EMP_STAT_UNEMPLOYED','LIFEEXP','PER_CAP_INC']]

    #get main data columns into separate dict and then a dataframe
    main_dict = r_dict['data']['main']
    df_main = pd.DataFrame(main_dict, index=[0])
    df_main = df_main[['RAW_E_DIESEL','RAW_E_CANCER','RAW_E_RESP','RAW_E_TRAFFIC','RAW_E_NPL','RAW_E_RMP','RAW_E_TSDF', 'RAW_E_O3', 'RAW_E_PM25', 'RAW_E_RSEI_AIR', 'totalPop', 'NUM_AIRPOLL']]

    #get extras columns into separate dict and then a dataframe
    extras_dict = r_dict['data']['extras']
    df_extras = pd.DataFrame(extras_dict, index=[0])
    df_extras = df_extras[['RAW_HI_ASTHMA', 'RAW_HI_CANCER', 'RAW_CI_FIRE', 'RAW_CI_FIRE30']]

    dfs = [df_dem, df_main, df_extras]

    df_final = ft.reduce(lambda left, right: pd.merge(left, right, left_index = True, right_index = True), dfs)

    # lower the column headers
    df_final.columns = map(str.lower, df_final.columns)
    df_final["latitude"] = lat
    df_final["longitude"] = lon
    
    
    return df_final
    

def acquire_safecast(city_dicts:dict,years:list,days_dict:dict, distance:int = 500):
    """Pulls from safecast data given the parameters below.

    Args:
        city_dicts (dict): dictionary of cities, latitude or longitude.
        years (list): A list of the years as integers.
        days_dict (dict): A dictionary of months and their respective day counts
        distance (int, optional): Distance for screen. Defaults to 500.

    Returns:
        pd.DataFrame: a dataframe with safecast data
    """    
    # loop through provided city's dictionary
    out_df = pd.DataFrame()
    for city in city_dicts:
        print(f"-- Acquiring data for Location ID: {city} --")
        city_df = pd.DataFrame()
        # loop through years that are provided
        for year in years:
            # loop through months that are provided
            for month in days_dict:
                print(f"Pulling Safecast data for: {month}/{year}")
                url = f'https://api.safecast.org/en-US/measurements?captured_after={year}%2F{month}%2F01+00%3A00%3A00&captured_before={year}%2F{month}%2F{days_dict[month]}+00%3A00%3A00&distance={distance}&format=json&latitude={city_dicts[city]["lat"]}&longitude={city_dicts[city]["long"]}'
                response = requests.get(url,verify=False)
                try:
                    df = pd.read_json(response.text)
                    city_df = pd.concat([city_df, df])
                    if len(city_df) == 0:
                        print(f"Data unavailable for {month}/{year}. Skipping month.")
                except:
                    print(f"Data unavailable for {month}/{year}. Skipping month.")
        city_df["city"] = city
        out_df = pd.concat([out_df, city_df])

        assert len(out_df) > 0, "There is no data for the selected years and location."
    return out_df

def compile(city_dicts:dict = city_dicts,years:list = [2019],month_num_start:int = 1,month_num_end:int = 6,distance:int = 500):
    """ Compiled safecast data with EJ screen data.
        - Allows filtering for years, months within those years, and distance
        - Pulls directly from API's using user provided information

    Args:
        city_dicts (dict, optional): dictionary of cities, latitude or longitude. Defaults to city_dicts.
        years (list, optional): A list of the years as integers. Defaults to [2019].
        month_num_start (int, optional): Starting month to be entered throughout the applied years. Defaults to 1.
        month_num_end (int, optional): Ending month to be entered throughout the applied years. Defaults to 6.
        distance (int, optional): Pulls from Safecast for specific distance. Defaults to 500.

    Returns:
        pd.DataFrame: DataFrame of compiled safecast / EJ screen data
    """    
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # if user selects specific months, filtering occurs here
    selected_months = days_in_month[(month_num_start-1):month_num_end]

    days_dict = {}
    for index, days in enumerate(selected_months):
        days_dict[str(index + 1).zfill(2)] = days # zfill adds the front 0's

    print("--- Safecast Data Pull --- \n")
    out_df = acquire_safecast(city_dicts, years, days_dict, distance)

    # must be of string type for ej screen function
    out_df["latitude"] = out_df["latitude"].astype(str)
    out_df["longitude"] = out_df["longitude"].astype(str)

    geo_loc = out_df[["latitude", "longitude"]].value_counts()
    unique_locations = [i for i in geo_loc.index]

    ejscreen_df = pd.DataFrame()
    print("--- EJ Screen Data Pull --- \n")
    for lat, lon in unique_locations:
        single_row_df = get_ejscreen_df(lat,lon,'3')
        ejscreen_df = pd.concat([ejscreen_df, single_row_df])

    merged_df = out_df.merge(ejscreen_df, how='left', on=["longitude", "latitude"])

    # filter out unwanted columns and return
    final_df = merged_df.drop(["location_name", "measurement_import_id","sensor_id","station_id","channel_id"])

    return final_df


def export_airquality_df_output(compiled_df:pd.DataFrame,file_loc:str = os.getcwd()):
    """exports a compiled EJ Screen / Safecast dataframe to a file location given

    Args:
        compiled_df (pd.DataFrame): a DataFrame of compiled EJ Screen / Safecast
        file_loc (str, optional): a string path for the file to be outputted to. Defaults to os.getcwd().
    """    
    unique_years = set([i.year for i in list(compiled_df["captured_at"])])
    output_file = f"{file_loc}/safecast_ej_output_{min(unique_years)}_{max(unique_years)}.csv"
    compiled_df.to_csv(output_file,index=False)
    print(f"file created: {output_file}\nThanks for using this tool!")


if __name__ == "__main__": 
    print("\n---- Welcome to the EJScreen - Safecast Data Compiler ---- \n")
    use_defaults = None
    defaults_options = {"y":True, "": True, "n":False}
    while use_defaults not in defaults_options:
        use_defaults = input("Would you like to continue with defaults? (This will create an output in the current directory you're in) [y]/n: ")
        try:
            defaults_options[use_defaults]
        except:
            print("Please enter either a 'y' or 'n'.")


    if defaults_options[use_defaults]:
        compiled_df = compile()
        export_airquality_df_output(compiled_df)
    else:
        
        city_dicts = {}
        enter_more = None
        while enter_more not in defaults_options:
            location_id = input("Enter a Location ID (ex: New York City, Los Angeles, etc.):\n")
            city_dicts[location_id] = {}
            city_dicts[location_id]["lat"] =  input(f"input a latitude for {location_id}:\n")
            city_dicts[location_id]["long"] =  input(f"input a longitude for {location_id}:\n")
            
            while True: 
                enter_more = input("Would you like to pull for another Location? [y]/n: ")
                try:
                    if not defaults_options[enter_more]:
                        break
                except:
                    print("Please enter either a 'y' or 'n'.")

        while True:
            try:
                start_year = int(input("Please enter a start year:\n"))
                end_year = int(input("Please enter an end year:\n"))
                month_num_start = int(input("Please enter the start month number to go through each year (ex: 1,2,...12):\n"))
                month_num_end = int(input("Please enter the end month number to go through each year (ex: 1,2,...12):\n"))
                distance = int(input("Please enter a distance for the safecast pull (suggested: 500+):\n"))
                break
            except:
                print("please enter a number.")

        years = list(range(start_year,end_year+1))

        print("Select an output directory in dialog box.")
        file_loc = askdirectory(title="Select an Output Directory")
        compiled_df = compile(city_dicts = city_dicts ,years = years ,month_num_start = month_num_start, month_num_end = month_num_end, distance= distance)
        export_airquality_df_output(compiled_df, file_loc)

