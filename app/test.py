import unittest
from django.test import TestCase


class MyTestCase(TestCase):
    def test_(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
