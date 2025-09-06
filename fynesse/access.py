import osmnx as ox

def get_osm_datapoints(latitude, longitude, box_size_km=2, poi_tags=None):
    """
    Retrieve OSM datapoints from a bounding box.

    Parameters
    ----------
    latitude, longitude : float
        Center point.
    box_size_km : float
        Bounding box size in kilometers.
    poi_tags : dict
        Dictionary of tags to query (e.g., {"amenity": True}).

    Returns
    -------
    GeoDataFrame or None
    """
    box_width = box_size_km / 111
    box_height = box_size_km / 111
    north = latitude + box_height
    south = latitude - box_height
    west = longitude - box_width
    east = longitude + box_width

    try:
        pois = ox.features_from_bbox(north, south, east, west, poi_tags)
        return pois
    except Exception as e:
        print(f"[Warning] OSM query failed: {e}")
        return None
