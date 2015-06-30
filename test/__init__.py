import unittest
from stl_reader import StlReader

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.__name__ = 'SRL reader Test Case'
        reader = StlReader()
        self.read_ascii = reader.read_ascii
