import unittest

from registrars.query import format_url


class CoordinateTestCase(unittest.TestCase):
    def test_hennepin(self):
        registrar_dict = {
            "url_format": ("https://gis.hennepin.us/Property/map/default.aspx?"
                           "C={coord1},{coord2}&L=7"),
            "coordinate_wkt": "+init=epsg:26915 +type=crs",
        }
        gps_location = (-93.3, 45.0)
        url = format_url(registrar_dict, gps_location)
        self.assertEqual(url,
                         "https://gis.hennepin.us/Property/map/default.aspx?"
                         "C=476355.4109102419,4982994.171200306&L=7")
