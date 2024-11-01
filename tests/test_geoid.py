from nsipy.nsi import get_geoid_nsi
import pytest
import geopandas


def test_rejects_invalid_geoid():
    with pytest.raises(ValueError, match="Invalid GEOID supplied"):
        get_geoid_nsi(123)

def test_returns_gdf_on_valid_geoid():
    assert type(get_geoid_nsi(150050319001015) == geopandas.geodataframe.GeoDataFrame)

def test_valid_length_nonexistant_geoid():
    x = get_geoid_nsi(12345)

    assert (type(x) == geopandas.geodataframe.GeoDataFrame and x.shape == (0, 1))