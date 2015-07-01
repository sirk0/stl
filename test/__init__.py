import unittest
from stl_reader import StlReader

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.__name__ = 'STL reader Test Case' #Needed for unittest.skip in Sublime Text
        reader = StlReader()
        self.read_ascii = reader.read_ascii
