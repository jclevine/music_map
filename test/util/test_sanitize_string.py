import unittest
from util.string_utils import sanitize_string


class SanitizeStringTest(unittest.TestCase):

    #===========================================================================
    # Test Lowercasing
    #===========================================================================
    def test_sanitize_lower_case(self):
        uppercased_string = "This IS a teST"
        expected_lowercased_string = 'this is a test'
        actual_string = sanitize_string(uppercased_string)
        self.assertEqual(expected_lowercased_string, actual_string)

    #===========================================================================
    # Test Removing The
    #===========================================================================
    def test_sanitize_remove_the(self):
        the_string = "This IS the teST"
        expected_no_the_string = 'this is test'
        actual_string = sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    def test_sanitize_remove_the_at_beginning(self):
        the_string = "THE This IS teST"
        expected_no_the_string = 'this is test'
        actual_string = sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    def test_sanitize_remove_the_at_beginning_no_space(self):
        the_string = "THEThis IS teST"
        expected_no_the_string = 'thethis is test'
        actual_string = sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    def test_sanitize_remove_the_at_end(self):
        the_string = "This IS teST the"
        expected_no_the_string = 'this is test'
        actual_string = sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    def test_sanitize_remove_the_at_end_no_space(self):
        the_string = "This IS teSTthe"
        expected_no_the_string = 'this is testthe'
        actual_string = sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    def test_sanitize_dont_remove_the_at_beginning_of_word(self):
        the_string = "The Low End Theory"
        expected_no_the_string = 'low end theory'
        actual_string = sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    #===========================================================================
    # Test Removing And
    #===========================================================================
    def test_sanitize_remove_and(self):
        and_string = "This IS And teST"
        expected_no_and_string = 'this is test'
        actual_string = sanitize_string(and_string, remove_and=True)
        self.assertEqual(expected_no_and_string, actual_string)

    def test_sanitize_remove_and_at_beginning(self):
        and_string = "ANd This IS teST"
        expected_no_and_string = 'this is test'
        actual_string = sanitize_string(and_string, remove_and=True)
        self.assertEqual(expected_no_and_string, actual_string)

    def test_sanitize_remove_and_at_beginning_no_space(self):
        and_string = "andThis IS teST"
        expected_no_and_string = 'andthis is test'
        actual_string = sanitize_string(and_string, remove_and=True)
        self.assertEqual(expected_no_and_string, actual_string)

    def test_sanitize_remove_and_at_end(self):
        and_string = "This IS teST anD"
        expected_no_and_string = 'this is test'
        actual_string = sanitize_string(and_string, remove_and=True)
        self.assertEqual(expected_no_and_string, actual_string)

    def test_sanitize_remove_and_at_end_no_space(self):
        and_string = "This IS teSTanD"
        expected_no_and_string = 'this is testand'
        actual_string = sanitize_string(and_string, remove_and=True)
        self.assertEqual(expected_no_and_string, actual_string)

    #===========================================================================
    # Test Removing The and And
    #===========================================================================
    def test_sanitize_remove_and_and_the(self):
        the_and_and_string = "This IS And teST the"
        expected_no_the_or_and_string = 'this is test'
        actual_string = sanitize_string(the_and_and_string, remove_the=True, remove_and=True)
        self.assertEqual(expected_no_the_or_and_string, actual_string)

    def test_sanitize_remove_and_and_the_adjacent(self):
        the_and_and_string = "ANd the This IS teST"
        expected_no_the_or_and_string = 'this is test'
        actual_string = sanitize_string(the_and_and_string, remove_the=True, remove_and=True)
        self.assertEqual(expected_no_the_or_and_string, actual_string)

    #===========================================================================
    # Test Sanitizing Strings with Periods
    #===========================================================================
    def test_sanitize_string_with_periods(self):
        string_with_periods = "Symphony No. 5 in C minor, Op. 67 Egmont Overture, Op.84"
        expected_string = 'symphony no 5 in c minor op 67 egmont overture op84'
        actual_string = sanitize_string(string_with_periods, remove_the=True, remove_and=True)
        self.assertEqual(expected_string, actual_string)

    #===========================================================================
    # Test Sanitizing Strings with Ampersands
    #===========================================================================
    def test_sanitize_string_with_ampersand(self):
        string_with_ampersand = 'Fevers & Mirrors'
        expected_string = 'fevers mirrors'
        actual_string = sanitize_string(string_with_ampersand, remove_the=True, remove_and=True)
        self.assertEqual(expected_string, actual_string)
