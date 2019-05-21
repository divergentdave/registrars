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
    epsg = registrar_dict.get("coordinate_epsg")
    if epsg is not None:
        epsg = int(epsg)
        proj = pyproj.Proj(init="epsg:{}".format(epsg))
        x, y = pyproj.transform(PROJ_WGS84, proj, *gps_location)
        return url_format.format(coord1=x, coord2=y)
    else:
        return url_format
