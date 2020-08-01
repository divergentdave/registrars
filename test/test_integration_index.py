import unittest

from registrars.build import build_index
from registrars.query import search_index


class IndexIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.index = build_index("test/data.yaml", None)

    def test_index(self):
        self.assertEqual(self.index.count((-180, -90, 180, 90)), 2)
        results = list(search_index((-93.3, 45.0), 0, self.index))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["osm_name"],
                         "Hennepin County, Minnesota, USA")

    def test_index_with_accuracy(self):
        results = list(search_index((-93.3, 45.0), 0.99, self.index))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["osm_name"],
                         "Hennepin County, Minnesota, USA")

        results = list(search_index((-93.3, 45.0), 5000, self.index))
        self.assertEqual(len(results), 1)

        results = list(search_index((-93.3, 45.0), 6000, self.index))
        self.assertEqual(len(results), 2)
