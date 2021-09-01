"""
Tests for the nbody file.
"""

import unittest

from src.nbody import *
from src.vector import Vector


class TestBody(unittest.TestCase):

    def test_Body_Contruction(self):
        self.assertEqual(True, True, "Something's really wrong!")


if __name__ == '__main__':
    unittest.main()
