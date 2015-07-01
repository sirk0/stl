from stl_reader import StlAsciiFormatError
from . import BaseTestCase

class TestStlReader(BaseTestCase):
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
        triangle = stl[0]
        exp_data = [0.062913, -0.004007, -0.998011,
                    0.62160000, -0.07850000, -4.96050000,
                    0.00000000, 0.00000000, -5.00000000,
                    0.62660000, 0.00000000, -4.96050000]
        self.assertEquals(triangle.normal.coords, exp_data[0:3])
        self.assertEquals(triangle[0].coords, exp_data[3:6])
        self.assertEquals(triangle[1].coords, exp_data[6:9])
        self.assertEquals(triangle[2].coords, exp_data[9:12])

    def test_non_existing(self):
        self.assertRaises(IOError, self.read_ascii, 'test/data/non_existing.stl')
