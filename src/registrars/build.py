import os
import pickle

import osmnx
from rtree import index
import yaml

osmnx.settings.use_cache = True


class BetterPicklingIndex(index.Index):
    def dumps(self, obj):
        return pickle.dumps(obj, -1)


def build_index(input_filename="../data.yaml", index_filename="../rtree"):
    with open(input_filename) as f:
        data = yaml.safe_load(f)

    rect_list = [None] * len(data)
    for i in range(len(data)):
        registrar_dict = data[i]
        osm_data = osmnx.osm_polygon_download(registrar_dict["osm_name"])[0]

        bounding_box = [float(coord) for coord in osm_data["boundingbox"]]
        bbox_south, bbox_north, bbox_west, bbox_east = bounding_box

        geojson = osm_data["geojson"]

        registrar_dict["id"] = i
        registrar_dict["geojson"] = geojson

        rect_list[i] = (
            i,
            (bbox_west, bbox_south, bbox_east, bbox_north),
            registrar_dict
        )

    if index_filename is None:
        return BetterPicklingIndex(rect_list)
    else:
        os.remove("{}.idx".format(index_filename))
        os.remove("{}.dat".format(index_filename))
        return BetterPicklingIndex(index_filename, rect_list)


if __name__ == "__main__":
    build_index()
