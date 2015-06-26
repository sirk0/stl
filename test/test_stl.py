from stl_reader import Stl, StlAsciiFormatError
import unittest

class TestSTL(unittest.TestCase):
    def test_read(self):
        result = Stl('test/data/cone_and_sphere.stl')
        self.assertTrue(len(result.data))

    def test_empty(self):
        self.assertRaises(StlAsciiFormatError, Stl, 'test/data/empty.stl')

    def test_wrong_start(self):
        self.assertRaises(StlAsciiFormatError, Stl, 'test/data/wrong_start.stl')
