import osmnx as ox
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from fynesse.access import get_osm_datapoints

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

def plot_city_map(place_name, latitude, longitude, box_size_km=2, poi_tags=None):
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

def get_osm_features(latitude, longitude, box_size_km=2, tags=None):
    """
    Access raw OSM features.
    """
    return get_osm_datapoints(latitude, longitude, box_size_km, tags)

def get_feature_vector(latitude, longitude, box_size_km=2, features=None):
    """
    Quantify geographic features into a feature vector.
    """

    # Build tags dict
    tags = {k: True for k, _ in features} if features else {}

    # Query OSM
    pois = get_osm_datapoints(latitude, longitude, box_size_km, tags)

    # Initialize with zeros
    all_features = [f"{k}:{v}" if v else k for k, v in features]
    feature_vec = {feat: 0 for feat in all_features}

    if pois is None or pois.empty:
        return feature_vec

    pois_df = pois.reset_index()

    for key, value in features:
        col_name = f"{key}:{value}" if value else key
        if key in pois_df.columns:
            if value:
                feature_vec[col_name] = pois_df[key].astype(str).str.lower().eq(str(value).lower()).sum()
            else:
                feature_vec[col_name] = pois_df[key].notna().sum()

    return feature_vec

def visualize_feature_space(X, y, method='PCA'):
    """
    Visualize feature space using PCA or t-SNE.
    """
    if method == 'PCA':
        reducer = PCA(n_components=2)
    elif method == 'tSNE':
        reducer = TSNE(n_components=2, random_state=42)
    else:
        raise ValueError("Method must be 'PCA' or 'tSNE'")

    X_reduced = reducer.fit_transform(X)
    plt.figure(figsize=(8, 6))
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap="tab10", alpha=0.7)
    plt.colorbar(label="Class")
    plt.title(f"Feature Space Visualization ({method})")
    plt.show()
