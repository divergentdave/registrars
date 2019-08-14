import pyproj
from rtree import index
import shapely.geometry

PROJ_WGS84 = pyproj.Proj(init="epsg:4326")


def open_index(name="rtree"):
    return index.Rtree(name)


def search_index(gps_location, index):
    longitude, latitude = gps_location
    query_bbox = (longitude, latitude, longitude, latitude)
    for registrar_dict in index.intersection(query_bbox, objects="raw"):
        polygon = shapely.geometry.shape(registrar_dict["geojson"])
        point = shapely.geometry.Point(*gps_location)
        if polygon.contains(point):
            yield registrar_dict


def format_url(registrar_dict, gps_location):
    url_format = registrar_dict.get("url_format")
    if url_format is None:
        return None
    wkt = registrar_dict.get("coordinate_wkt")
    if wkt is not None:
        epsilon = float(registrar_dict.get("epsilon", "0"))
        proj = pyproj.Proj(wkt)
        x, y = pyproj.transform(PROJ_WGS84, proj, *gps_location)
        return url_format.format(
            coord1=x,
            coord2=y,
            coord1_minus_epsilon=x - epsilon,
            coord2_minus_epsilon=y - epsilon,
            coord1_plus_epsilon=x + epsilon,
            coord2_plus_epsilon=y + epsilon,
        )
    else:
        return url_format
