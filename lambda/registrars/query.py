import math

import pyproj
from rtree import index
import shapely.geometry

PROJ_WGS84 = pyproj.Proj("epsg:4326")
METERS_PER_DEGREE = 111111


def degrees_to_radians(degrees):
    return degrees / 180 * math.pi


def open_index(name="rtree"):
    return index.Rtree(name)


def search_index(gps_location, accuracy, index):
    longitude, latitude = gps_location
    if accuracy:
        accuracy = abs(accuracy)
        dlat = accuracy / METERS_PER_DEGREE
        latitude_rad = degrees_to_radians(latitude)
        dlon = accuracy / (METERS_PER_DEGREE * math.cos(latitude_rad))
        query_bbox = (
            longitude - dlon,
            latitude - dlat,
            longitude + dlon,
            latitude + dlat
        )
        for registrar_dict in index.intersection(query_bbox, objects="raw"):
            polygon = registrar_dict["geometry"]
            square = shapely.geometry.Polygon([
                (longitude - dlon, latitude - dlat),
                (longitude - dlon, latitude + dlat),
                (longitude + dlon, latitude + dlat),
                (longitude + dlon, latitude - dlat),
            ])
            if polygon.intersects(square):
                yield registrar_dict
    else:
        query_bbox = (longitude, latitude, longitude, latitude)
        for registrar_dict in index.intersection(query_bbox, objects="raw"):
            polygon = registrar_dict["geometry"]
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
        transformer = pyproj.Transformer.from_proj(PROJ_WGS84, proj)
        x, y = transformer.transform(gps_location[1], gps_location[0])
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
