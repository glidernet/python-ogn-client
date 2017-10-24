import unittest

from ogn.parser.parse_naviter import parse


class TestStringMethods(unittest.TestCase):
    def test_OGCAPT(self):
        message = parse(" ")

        self.assertEqual(message['Capture'], "YES")


if __name__ == '__main__':
    unittest.main()
