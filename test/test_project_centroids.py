import unittest

import shapely.geometry
import yaml

from registrars.query import open_index, format_url


class ProjectAllCentroids(unittest.TestCase):
    def test_project(self):
        index = open_index("lambda/rtree")
        bounds = index.get_bounds(False)
        count = 0
        for registrar_dict in index.intersection(bounds, objects="raw"):
            count += 1
            polygon = shapely.geometry.shape(registrar_dict["geojson"])
            url = format_url(registrar_dict, list(*polygon.centroid.coords))
            assert "inf" not in url
        if count == 0:
            raise Exception("No registrars found in main index")
