import os
import pickle

import osmnx
from rtree import index
import yaml

osmnx.settings.use_cache = True


class BetterPicklingIndex(index.Index):
    def dumps(self, obj):
        return pickle.dumps(obj, -1)


def build_index():
    data = yaml.safe_load(open("data.yaml"))

    rect_list = [None] * len(data)
    for i in range(len(data)):
        registrar_dict = data[i]
        osm_data = osmnx.osm_polygon_download(registrar_dict["osm_name"])[0]
        bounding_box = [float(coord) for coord in osm_data["boundingbox"]]
        bbox_south, bbox_north, bbox_west, bbox_east = bounding_box
        rect_list[i] = (
            i,
            (bbox_west, bbox_south, bbox_east, bbox_north),
            registrar_dict
        )

    os.remove("rtree.idx")
    os.remove("rtree.dat")
    BetterPicklingIndex("rtree", rect_list)


if __name__ == "__main__":
    build_index()
