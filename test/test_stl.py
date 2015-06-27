from stl_reader import StlReader, StlAsciiFormatError
import unittest

class TestSTL(unittest.TestCase):
    def setUp(self):
        self.reader = StlReader()
        self.read_ascii = self.reader.read_ascii

    def test_read(self):
        stl = self.read_ascii('test/data/cone_and_sphere.stl')
        self.assertEquals(len(stl), 2430)

    def test_empty(self):
        self.assertRaises(StlAsciiFormatError, self.read_ascii, 'test/data/empty.stl')

    def test_wrong_start(self):
        self.assertRaises(StlAsciiFormatError, self.read_ascii, 'test/data/wrong_start.stl')

    def test_one_triangle(self):
        stl = self.read_ascii('test/data/one_triangle.stl')
        self.assertEquals(len(stl), 1)
        triangle = stl.triangles[0]
        exp_data = [0.062913, -0.004007, -0.998011, 
                    0.62160000, -0.07850000, -4.96050000,
                    0.00000000, 0.00000000, -5.00000000,
                    0.62660000, 0.00000000, -4.96050000]
        self.assertEquals(triangle.normal, exp_data[0:3])
        self.assertEquals(triangle.point1, exp_data[3:6])
        self.assertEquals(triangle.point2, exp_data[6:9])
        self.assertEquals(triangle.point3, exp_data[9:12])
