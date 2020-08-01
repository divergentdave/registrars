import os
import pickle

import osmnx
from rtree import index
import yaml

osmnx.settings.use_cache = True
osmnx.settings.cache_folder = "../cache"

ALLOWED_KEYS = {
    "osm_name",
    "url_format",
    "coordinate_wkt",
    "epsilon",
}
DROP_KEYS = {
    "software",
}


class BetterPicklingIndex(index.Index):
    def dumps(self, obj):
        return pickle.dumps(obj, -1)


def clean_registrar_dict(registrar_dict):
    registrar_dict = dict(
        (key, value) for (key, value) in registrar_dict.items()
        if key not in DROP_KEYS
    )
    for key in registrar_dict:
        if key not in ALLOWED_KEYS:
            raise Exception("Unexpected key: {}".format(key))
    return registrar_dict


def build_index(input_filename="../data.yaml", index_filename="rtree"):
    with open(input_filename) as f:
        data = yaml.safe_load(f)

    rect_list = [None] * len(data)
    for i in range(len(data)):
        registrar_dict = clean_registrar_dict(data[i])
        gdf = osmnx.geocode_to_gdf(registrar_dict["osm_name"])
        if len(gdf) == 0:
            raise Exception("Couldn't find geometry for {}"
                            .format(registrar_dict["osm_name"]))
        geometry = gdf.geometry[0]
        bbox_north = gdf.bbox_north[0]
        bbox_south = gdf.bbox_south[0]
        bbox_east = gdf.bbox_east[0]
        bbox_west = gdf.bbox_west[0]

        registrar_dict["id"] = i
        registrar_dict["geometry"] = geometry

        rect_list[i] = (
            i,
            (bbox_west, bbox_south, bbox_east, bbox_north),
            registrar_dict
        )

    if index_filename is None:
        return BetterPicklingIndex(rect_list)
    else:
        for filename in ("{}.idx".format(index_filename),
                         "{}.dat".format(index_filename)):
            if os.path.isfile(filename):
                os.remove(filename)
        return BetterPicklingIndex(index_filename, rect_list)


if __name__ == "__main__":
    build_index()
