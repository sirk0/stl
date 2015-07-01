from stl_reader import BoundingBox, Point, Triangle, Stl
from . import BaseTestCase

class TestPoint(BaseTestCase):
    def test_point_equals(self):
        point1 = Point([1, 2, 3])
        point2 = Point([1.0, 2.0, 3.0])
        self.assertTrue(point1 == point2)

    def test_point_not_equals(self):
        point1 = Point([1, 2, 3])
        point2 = Point([1.0, 2.0, 3.1])
        self.assertFalse(point1 == point2)

    def test_point_boundain_box(self):
        point = Point([1, 2, 3])
        self.assertEquals(point.bounding_box.min, point)
        self.assertEquals(point.bounding_box.max, point)

class TestBoundingBox(BaseTestCase):
    def test_in(self):
        point1 = Point([1, 2, 3])
        point2 = Point([4, 5, 6])
        bounding_box = BoundingBox(point1, point2)

        point3 = Point([4, 4, 4])
        point4 = Point([3, 2, 1])

        self.assertTrue(point3 in bounding_box)
        self.assertFalse(point4 in bounding_box)

    def test_add(self):
        point1 = Point([1, 2, 3])
        point2 = Point([3, 2, 1])
        point_min = Point([1, 2, 1])
        point_max = Point([3, 2, 3])

        bounding_box = point1.bounding_box + point2.bounding_box

        self.assertEquals(bounding_box.min, point_min)
        self.assertEquals(bounding_box.max, point_max)

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
        normal = [0, 0, 1]
        point1 = Point([1, 2, 3])
        point2 = Point([3, 2, 1])
        point3 = Point([2, 2, 2])
        point_min = Point([1, 2, 1])
        point_max = Point([3, 2, 3])

        triangle = Triangle(normal, point1, point2, point3)

        self.assertEquals(triangle.bounding_box.min, point_min)
        self.assertEquals(triangle.bounding_box.max, point_max)

    def test_area(self):
        normal = [0, 0, 1]
        point1 = Point([0, 0, 0])
        point2 = Point([0, 0, 2])
        point3 = Point([0, 2, 0])
        triangle = Triangle(normal, point1, point2, point3)

        self.assertEquals(triangle.get_area(), 2)

class TestStl(BaseTestCase):
    def test_contacts_triangle(self):
        stl = self.read_ascii('test/data/separate_triangles.stl')
        triangle = stl[0]
        self.assertTrue(stl.contacts_triangle(triangle))

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
        point_min = Point([0, -0.0785, -5])
        point_max = Point([10, 15, 0])

        self.assertEquals(stl.bounding_box.min, point_min)
        self.assertEquals(stl.bounding_box.max, point_max)

    def test_area(self):
        normal = [0, 0, 1]
        point1 = Point([0, 0, 0])
        point2 = Point([0, 0, 2])
        point3 = Point([0, 2, 0])
        triangle = Triangle(normal, point1, point2, point3)
        stl = Stl([triangle, triangle])

        self.assertEquals(stl.get_area(), 4)
