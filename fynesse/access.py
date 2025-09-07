import osmnx as ox

def get_osm_datapoints(latitude, longitude, box_size_km=2, poi_tags=None):

    tags = {
    "amenity": True,
    "buildings": True,
    "historic": True,
    "leisure": True,
    "shop": True,
    "tourism": True,
    "religion": True,
    "memorial": True}


    box_width = box_size_km / 111
    box_height = box_size_km / 111
    north = latitude + box_height
    south = latitude - box_height
    west = longitude - box_width
    east = longitude + box_width
    # tags = poi_tags or {}
    print("working")
    # try:
    #     bbox = (west, south, east, north)
    #     pois = ox.features_from_bbox(bbox, poi_tags=tags)
    #     return pois
    # except Exception as e:
    #     print(f"[Warning] OSM query failed: {e}")
    #     return None


