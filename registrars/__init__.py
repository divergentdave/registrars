import osmnx
import pyproj
import yaml

osmnx.settings.use_cache = True

PROJ_WGS84 = pyproj.Proj(init="epsg:4326")

DATA = yaml.safe_load(open("data.yaml"))


def format_url(registrar_dict, gps_location):
    url_format = registrar_dict.get("url_format")
    if url_format is None:
        return None
    if "epsg" in registrar_dict:
        epsg = int(registrar_dict["epsg"])
        proj = pyproj.Proj(init="epsg:{}".format(epsg))
        x, y = pyproj.transform(PROJ_WGS84, proj, *gps_location)
        return url_format.format(coord1=x, coord2=y)
    else:
        return url_format
