import unittest

import requests
import shapely.geometry

from registrars.query import open_index, format_url


class LinkCheck(unittest.TestCase):
    @unittest.skip("Expensive network requests")
    def test_link_check(self):
        index = open_index("lambda/rtree")
        bounds = index.get_bounds(False)
        for registrar_dict in index.intersection(bounds, objects="raw"):
            polygon = shapely.geometry.shape(registrar_dict["geojson"])
            url = format_url(registrar_dict, list(*polygon.centroid.coords))
            resp = requests.get(url)
            resp.raise_for_status()