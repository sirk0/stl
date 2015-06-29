from stl_reader import BoundingBox, Point, Triangle, Stl, StlReader, StlAsciiFormatError
import unittest

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.__name__ = 'SRL reader Test Case'
        reader = StlReader()
        self.read_ascii = reader.read_ascii

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

class TestPoint(BaseTestCase):
    def test_point_equals(self):
        p1 = Point([1,2,3])
        p2 = Point([1.0,2.0,3.0])
        self.assertTrue(p1 == p2)

    def test_point_not_equals(self):
        p1 = Point([1,2,3])
        p2 = Point([1.0,2.0,3.1])
        self.assertFalse(p1 == p2)

    def test_point_boundain_box(self):
        point = Point([1,2,3])
        self.assertEquals(point.bounding_box.min, point)
        self.assertEquals(point.bounding_box.max, point)

def TestBoundingBox(BaseTestCase):
    def test_in(self):
        p1 = Point([1,2,3])
        p2 = Point([4,5,6])
        bounding_box = BoundingBox(p1, p2)

        p3 = Point([4,4,4])
        p4 = Point([3,2,1])

        self.assertTrue(p3 in bounding_box)
        self.assertFalse(p4 in bounding_box)

    def test_add(self):
        p1 = Point([1,2,3])
        p2 = Point([3,2,1])
        p_min = Point([1,2,1])
        p_max = Point([3,2,2])

        bounding_box = p1.bounding_box + p2.bounding_box

        self.assertEquals(bounding_box.min, p_min)
        self.assertEquals(bounding_box.max, p_max)

class TestTriangle(BaseTestCase):
    def test_contacts(self):
        stl = self.read_ascii('test/data/contacting_triangles.stl')
        triangle1 = stl[0]
        triangle2 = stl[1]
        self.assertTrue(triangle1.contacts(triangle2))

    def test_does_not_contact(self):
        stl = self.read_ascii('test/data/separate_triangles.stl')
        triangle1 = stl[0]
        triangle2 = stl[1]
        self.assertFalse(triangle1.contacts(triangle2))

    def test_bounding_box(self):
        normal = [0,0,1]
        p1 = Point([1,2,3])
        p2 = Point([3,2,1])
        p3 = Point([2,2,2])
        p_min = Point([1,2,1])
        p_max = Point([3,2,3])

        t = Triangle(normal, p1, p2, p3)

        self.assertEquals(t.bounding_box.min, p_min)
        self.assertEquals(t.bounding_box.max, p_max)

class TestStl(BaseTestCase):
    def test_contacts_triangle(self):
        stl = self.read_ascii('test/data/separate_triangles.stl')
        triangle1 = stl[0]
        triangle2 = stl[1]
        self.assertTrue(stl.contacts_triangle(triangle1))

    def test_does_not_contact_triangle(self):
        stl = self.read_ascii('test/data/separate_triangles.stl')
        stl1 = Stl([stl[0]])
        self.assertFalse(stl1.contacts_triangle(stl[1]))

    def test_contacts_stl(self):
        stl1 = self.read_ascii('test/data/separate_triangles.stl')
        stl2 = self.read_ascii('test/data/separate_triangles.stl')
        self.assertTrue(stl1.contacts_stl(stl2))

    def test_does_not_contact_stl(self):
        stl = self.read_ascii('test/data/separate_triangles.stl')
        stl1 = Stl([stl[0]])
        stl2 = Stl([stl[1]])
        self.assertFalse(stl1.contacts_stl(stl2))

    def test_bounding_box(self):
        stl = self.read_ascii('test/data/separate_triangles.stl')
        p_min = Point([0, -0.0785, -5])
        p_max = Point([10,15,0])

        self.assertEquals(stl.bounding_box.min, p_min)
        self.assertEquals(stl.bounding_box.max, p_max)

    @unittest.skip
    def test_split_surfaces(self):
        stl = self.read_ascii('test/data/cone_and_sphere.stl')
        split_stls = stl.split_surfaces()
        self.assertEquals(len(split_stls), 2)
