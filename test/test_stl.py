from stl_reader import Stl, StlAsciiFormatError
import unittest

class TestSTL(unittest.TestCase):
    def test_read(self):
        stl = Stl('test/data/cone_and_sphere.stl')
        self.assertTrue(len(stl.data))

    def test_empty(self):
        self.assertRaises(StlAsciiFormatError, Stl, 'test/data/empty.stl')

    def test_wrong_start(self):
        self.assertRaises(StlAsciiFormatError, Stl, 'test/data/wrong_start.stl')

    def test_one_triangle(self):
        stl = Stl('test/data/one_triangle.stl')
        self.assertEquals(len(stl.data), 1)
        exp_data = [0.062913, -0.004007, -0.998011, 
                    0.62160000, -0.07850000, -4.96050000,
                    0.00000000, 0.00000000, -5.00000000,
                    0.62660000, 0.00000000, -4.96050000]
        self.assertEquals(stl.data[0], exp_data)
