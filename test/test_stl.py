from stl_reader import read_stl_ascii, StlAsciiFormatError
import unittest

class TestSTL(unittest.TestCase):
    def test_read(self):
        read_stl_ascii('test/data/cone_and_sphere.stl')

    def test_empty(self):
        self.assertRaises(StlAsciiFormatError, read_stl_ascii, 'test/data/empty.stl')

    def test_wrong_start(self):
        self.assertRaises(StlAsciiFormatError, read_stl_ascii, 'test/data/wrong_start.stl')
    