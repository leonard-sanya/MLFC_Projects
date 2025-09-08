import osmnx as ox
import matplotlib.pyplot as plt

features = [
    ("building", None),
    ("amenity", None),
    ("amenity", "school"),
    ("amenity", "hospital"),
    ("amenity", "restaurant"),
    ("amenity", "cafe"),
    ("shop", None),
    ("tourism", None),
    ("tourism", "hotel"),
    ("tourism", "museum"),
    ("leisure", None),
    ("leisure", "park"),
    ("historic", None),
    ("amenity", "place_of_worship"),]


tags = {k: True for k, _ in features} if features else {}

def get_osm_datapoints(latitude, longitude, box_size_km=2, poi_tags=None):

  
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

    box_width = box_size_km / 111  # ~1° lat ≈ 111 km
    box_height = box_size_km / 111
    north = latitude + box_height
    south = latitude - box_height
    west = longitude - box_width
    east = longitude + box_width
    bbox = (west, south, east, north)  


    graph = ox.graph_from_bbox(bbox)
    area = ox.geocode_to_gdf(place_name)
    nodes, edges = ox.graph_to_gdfs(graph)

    try:
        buildings = ox.features_from_bbox(bbox,tags={"building": True})
        pois = ox.features_from_bbox(bbox, tags)

        fig, ax = plt.subplots(figsize=(6,6))
        area.plot(ax=ax, color="tan", alpha=0.5)
        buildings.plot(ax=ax, facecolor="gray", edgecolor="gray")
        edges.plot(ax=ax, linewidth=1, edgecolor="black", alpha=0.3)
        nodes.plot(ax=ax, color="black", markersize=1, alpha=0.3)
        pois.plot(ax=ax, color="green", markersize=5, alpha=1)
        ax.set_xlim(west, east)
        ax.set_ylim(south, north)
        ax.set_title(place_name, fontsize=14)
        plt.show()

    except Exception as e:
        print(f"[Warning] Could not plot map: {e}")


def plot_city_map2(place_name, latitude, longitude, box_size_km=2, poi_tags=None):
    """
    Plot city map with OSM data overlay.
    """

    box_width = box_size_km / 111
    box_height = box_size_km / 111
    north = latitude + box_height
    south = latitude - box_height
    west = longitude - box_width
    east = longitude + box_width
    bbox = (west, south, east, north)

    try:
        pois = ox.features_from_bbox(bbox, tags)
        fig, ax = ox.plot_footprints(ox.geocode_to_gdf(place_name), figsize=(8, 8), show=False, close=False)
        pois.plot(ax=ax, color="red", markersize=5)
        plt.title(f"Points of Interest in {place_name}")
        plt.show()
    except Exception as e:
        print(f"[Warning] Could not plot map: {e}")