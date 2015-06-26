from stl_reader import read_stl_ascii, AsciiFormatError
import unittest

class TestSTL(unittest.TestCase):
    def test_read(self):
        read_stl_ascii('test/data/cone_and_sphere.stl')

    def test_empty(self):
        self.assertRaises(AsciiFormatError, read_stl_ascii, 'test/data/empty.stl')