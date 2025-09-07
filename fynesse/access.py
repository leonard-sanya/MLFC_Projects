import osmnx as ox
import geopandas as gpd
from shapely.geometry import box

def get_osm_datapoints(latitude, longitude, box_size_km=2, poi_tags=None):
    """
    Retrieve OSM datapoints from a bounding box (compatible with OSMnx v2.0.6).
    """

    tags = poi_tags or {
        "amenity": True,
        "building": True,
        "historic": True,
        "leisure": True,
        "shop": True,
        "tourism": True,
        "religion": True,
        "memorial": True,
    }

    # bounding box size in degrees
    box_width = box_size_km / 111
    box_height = box_size_km / 111
    north = latitude + box_height
    south = latitude - box_height
    west = longitude - box_width
    east = longitude + box_width

    # Create shapely bounding box
    bbox_polygon = box(west, south, east, north)
    gdf = gpd.GeoDataFrame(geometry=[bbox_polygon], crs="EPSG:4326")

    try:
        pois = ox.features_from_polygon(gdf.loc[0, "geometry"], tags=tags)
        print(f"[Info] Retrieved {len(pois)} features from OSM.")
        return pois
    except Exception as e:
        print(f"[Warning] OSM query failed: {e}")
        return gpd.GeoDataFrame()  # empty fallback
