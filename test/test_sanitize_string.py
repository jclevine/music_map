import unittest
from music_map import MusicMap


class SanitizeStringTest(unittest.TestCase):

    def test_sanitize_lower_case(self):
        uppercased_string = "This IS a teST"
        expected_lowercased_string = 'this is a test'
        actual_string = MusicMap.sanitize_string(uppercased_string)
        self.assertEqual(expected_lowercased_string, actual_string)
