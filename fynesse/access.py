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
  
    try:
        bbox = (west, south, east, north)
        pois = ox.features_from_bbox(bbox, tags=tags)
        return pois.head()

    except Exception as e:
        print(f"[Warning] OSM query failed: {e}")
        return None

def plot_city_map(place_name, latitude, longitude, box_size_km=2, poi_tags=None):
    """
    Plot city map with OSM data overlay using a bounding box.
    """

    # --- compute bounding box ---
    box_width = box_size_km / 111  # ~1° lat ≈ 111 km
    box_height = box_size_km / 111
    north = latitude + box_height
    south = latitude - box_height
    west = longitude - box_width
    east = longitude + box_width
    bbox = (north, south, east, west)  

    try:
        buildings = ox.features_from_bbox(north, south, east, west, tags={"building": True})
        pois = ox.features_from_bbox(north, south, east, west, tags=poi_tags or {"amenity": True})

        fig, ax = plt.subplots(figsize=(8, 8))
        buildings.plot(ax=ax, facecolor="lightgrey", alpha=0.7)
        pois.plot(ax=ax, color="red", markersize=5)

        plt.title(f"Points of Interest in {place_name}")
        plt.show()

    except Exception as e:
        print(f"[Warning] Could not plot map: {e}")

