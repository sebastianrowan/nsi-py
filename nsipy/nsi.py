import os
import sys
import requests
import json
from pandas import DataFrame, json_normalize
import geopandas
from geopandas import GeoDataFrame, GeoSeries

URL = "https://nsi.sec.usace.army.mil/nsiapi/"


def get_geoid_nsi(geoid: str | int) -> GeoDataFrame:
    """Get NSI structures located within the geography defined by the given GEOID

    Args:
        geoid (str | int): Geographic identifier of the state, county, tract, block group, or block for which you are requesting data

    Returns:
        GeoDataFrame: GeoDataFrame containing NSI data for requested location
    """
    geoid = str(geoid)
    if len(geoid) < 5:
        if len(geoid) == 1:
            geoid = f"0{geoid}"
        if len(geoid) == 2:
            print("It is recommended to use the `get_state_nsi()` function to download a statewide dataset.")

    if not len(geoid) in [2, 5, 11, 12, 15]: 
        raise ValueError("Invalid GEOID supplied")

    request_url = f"{URL}/structures?fips={geoid}"
    
    try:
        r = requests.get(request_url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    
    try:
        nsi = geopandas.read_file(r.text)
    except:
        nsi = geopandas.read_file(r.text, driver='GeoJSON')

    return(nsi)
            

def get_shp_nsi(shp: GeoDataFrame) -> GeoDataFrame:
    """
    Get NSI structures located within the boundaries of a given polygon layer

    Parameters
    ----------
    shp : GeoDataFrame
    
    Returns
    -------
    GeoDataFrame: GeoDataFrame containing NSI data for requested location
    """

    request_url = f"{URL}/structures?fmt=fc"

    #TODO: Add option to automatically join attributes from features in input polygon to NSI result
    #   This could be implemented by spatial join after returning results, or by 
    #   splitting up the API call for each feature in the input and appending the attributes for the
    #   current polygon to the results and merging all the results at the end.  

    try:
        r = requests.post(url = request_url, data = shp.dissolve().to_json())
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
        
    try:
        nsi = geopandas.read_file(r.text)
    except:
        nsi = geopandas.read_file(r.text, driver='GeoJSON')

    return(nsi)


def get_bbox_nsi(extent: tuple, stats_only: bool = False) -> GeoDataFrame| DataFrame:
    """Get NSI structures located within the given bounding box

    Args:
        extent (tuple): Tuple of coordinates defining the extents of the bounding box (min_x, max_x, min_y, max_y)
        stats_only (bool, optional): If True, return DataFrame containing only the statistics of the NSI data in
        the specified bounding box. Otherwise, returns GeoDataFrame with NSI points. Defaults to False.

    Returns:
        GeoDataFrame | DataFrame: GeoDataFrame containing NSI data or DataFrame containing NSI stats for requested location.
    """
    west = extent[0]
    east = extent[1]
    south = extent[2]
    north = extent[3]
    bbox = f"{west},{south},{west},{north},{east},{north},{east},{south},{west},{south}"
 

    #TODO: check that bbox is within the US

    if stats_only:
        request_url = f"{URL}/stats?bbox={bbox}&fmt=fc"
    else:
        request_url = f"{URL}/structures?bbox={bbox}&fmt=fc"

    try:
        r = requests.get(request_url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    
    if stats_only:
        nsi = json_normalize(json.loads(r.text))
    else:
        try:
            nsi = geopandas.read_file(r.text)
        except:
            nsi = geopandas.read_file(r.text, driver='GeoJSON')

    return(nsi)


def get_state_nsi(state: str, save_path: str = None) ->  str:
    """Download a geopackage of NSI data for the specified state

    Args:
        state (str): GEOID of state for which you are requesting the dataset
        save_path (str, optional): location to save the NSI geopackage. If None, saves to the current working
            directory. Defaults to None.

    Returns: 
        str: full path for the saved geopackage
    """
    state = str(state)

    valid_states = ['01', '02', '04', '05', '06', '08', '09', '10', '11', '12', '13', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56']

    if len(state) == 1:
        state = f"0{state}"

    if not state in valid_states:
        raise ValueError("Invalid state GEIOD supplied. For a list of valid state codes, see: https://www.census.gov/library/reference/code-lists/ansi.html#states")
    
    #TODO: should probably handle case where user only provides a directory
    ##  That case should raise an error
    if save_path is None:
        save_path = os.path.join(os.getcwd(), f"nsi_2022_{state}.gpkg.zip")

    if os.path.isdir(save_path):
        raise IsADirectoryError

    if not save_path.endswith(".gpkg.zip"):
        save_path = f"{save_path}.gpkg.zip"

    request_url = f"https://nsi.sec.usace.army.mil/downloads/nsi_2022/nsi_2022_{state}.gpkg.zip"

    try:
        r = requests.get(url = request_url, stream = True)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
    with open(save_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    return(save_path)