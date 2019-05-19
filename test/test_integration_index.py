import unittest

from registrars.build import build_index
from registrars.query import search_index


class IndexIntegrationTestCase(unittest.TestCase):
    def test_index(self):
        index = build_index("test/data.yaml", None)
        self.assertEqual(index.count((-180, -90, 180, 90)), 1)
        results = list(search_index((-93.3, 45.0), index))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["osm_name"],
                         "Hennepin County, Minnesota, USA")
