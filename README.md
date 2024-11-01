# nsipy

Python package to download data from the U.S. Army Corps of Engineers National Structures Inventory using the NSI API.

## Installation

`nsipy` can be installed using pip:

```
pip install nsipy
```

## Usage

```
from nsipy import nsi
```

`get_geoid_nsi()` returns NSI data for a specific GEOID/FIPS code:

```
# get NSI data for Strafford County, New Hampshire (GEOID = 33017)
nsi_nh_strafford = nsi.get_geoid_nsi(33017)

print(nsi_nh_strafford.head())
```

|   | fd_id     | occtype   | ... | ground_elv | ground_elv_m | geometry                   |
| - | --------- | --------- | --- | ---------- | ------------ | -------------------------- |
| 0 | 548050978 | RES1-2SNB | ... | 175.700982 | 53.553658    | POINT (-71.00779 43.15282) |
| 1 | 548053375 | RES3A     | ... | 37.394929  | 11.397974    | POINT (-70.8517 43.16478)  |
| 2 | 548053423 | RES1-2SNB | ... | 38.221904  | 11.650036    | POINT (-70.852 43.16468)   |
| 3 | 548054430 | RES1-1SWB | ... | 121.293660 | 36.970306    | POINT (-70.82112 43.23762) |
| 4 | 548056959 | RES3      | ... | 80.907904  | 24.660728    | POINT (-70.89252 43.16359) |


`get_shp_nsi()` returns NSI data for the area within a specified polygon layer (GeoDataFrame). If the dataframe contains multiple rows (features), the features will be dissolved into a single polygon before sending the API call so the entire area will be returned. If you wish to get NSI data for a specific feature(s), first filter the GeoDataFrame as shown below.

```
import geopandas as gpd

# Load polygon containing all New Hampshire town boundaries as GeoPandas GeoDataFrame
nh_towns = gpd.read_file('path/to/file/New_Hampshire_Political_Boundaries.geojson')

# Filter layer to strafford county towns
strafford_county_towns = nh_counties[[nh_counties['pbpCOUNTY'] == 17]]

# Get NSI data for Straffod County using layer
nsi_nh_strafford = nsi.get_shp_nsi(strafford_county_towns)

print(nsi_nh_strafford.head())
```

|   | fd_id     | occtype   | ... | ground_elv | ground_elv_m | geometry                   |
| - | --------- | --------- | --- | ---------- | ------------ | -------------------------- |
| 0 | 548050978 | RES1-2SNB | ... | 175.700982 | 53.553658    | POINT (-71.00779 43.15282) |
| 1 | 548053375 | RES3A     | ... | 37.394929  | 11.397974    | POINT (-70.8517 43.16478)  |
| 2 | 548053423 | RES1-2SNB | ... | 38.221904  | 11.650036    | POINT (-70.852 43.16468)   |
| 3 | 548054430 | RES1-1SWB | ... | 121.293660 | 36.970306    | POINT (-70.82112 43.23762) |
| 4 | 548056959 | RES3      | ... | 80.907904  | 24.660728    | POINT (-70.89252 43.16359) |