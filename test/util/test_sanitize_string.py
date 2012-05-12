import unittest
from util import string_utils


class SanitizeStringTest(unittest.TestCase):

    #===========================================================================
    # Test Lowercasing
    #===========================================================================
    def test_sanitize_lower_case(self):
        uppercased_string = "This IS a teST"
        expected_lowercased_string = 'this is a test'
        actual_string = string_utils.sanitize_string(uppercased_string)
        self.assertEqual(expected_lowercased_string, actual_string)

    #===========================================================================
    # Test Removing The
    #===========================================================================
    def test_sanitize_remove_the(self):
        the_string = "This IS the teST"
        expected_no_the_string = 'this is test'
        actual_string = string_utils.sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    def test_sanitize_remove_the_at_beginning(self):
        the_string = "THE This IS teST"
        expected_no_the_string = 'this is test'
        actual_string = string_utils.sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    def test_sanitize_remove_the_at_beginning_no_space(self):
        the_string = "THEThis IS teST"
        expected_no_the_string = 'thethis is test'
        actual_string = string_utils.sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    def test_sanitize_remove_the_at_end(self):
        the_string = "This IS teST the"
        expected_no_the_string = 'this is test'
        actual_string = string_utils.sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    def test_sanitize_remove_the_at_end_no_space(self):
        the_string = "This IS teSTthe"
        expected_no_the_string = 'this is testthe'
        actual_string = string_utils.sanitize_string(the_string, remove_the=True)
        self.assertEqual(expected_no_the_string, actual_string)

    #===========================================================================
    # Test Removing And
    #===========================================================================
    def test_sanitize_remove_and(self):
        and_string = "This IS And teST"
        expected_no_and_string = 'this is test'
        actual_string = string_utils.sanitize_string(and_string, remove_and=True)
        self.assertEqual(expected_no_and_string, actual_string)

    def test_sanitize_remove_and_at_beginning(self):
        and_string = "ANd This IS teST"
        expected_no_and_string = 'this is test'
        actual_string = string_utils.sanitize_string(and_string, remove_and=True)
        self.assertEqual(expected_no_and_string, actual_string)

    def test_sanitize_remove_and_at_beginning_no_space(self):
        and_string = "andThis IS teST"
        expected_no_and_string = 'andthis is test'
        actual_string = string_utils.sanitize_string(and_string, remove_and=True)
        self.assertEqual(expected_no_and_string, actual_string)

    def test_sanitize_remove_and_at_end(self):
        and_string = "This IS teST anD"
        expected_no_and_string = 'this is test'
        actual_string = string_utils.sanitize_string(and_string, remove_and=True)
        self.assertEqual(expected_no_and_string, actual_string)

    def test_sanitize_remove_and_at_end_no_space(self):
        and_string = "This IS teSTanD"
        expected_no_and_string = 'this is testand'
        actual_string = string_utils.sanitize_string(and_string, remove_and=True)
        self.assertEqual(expected_no_and_string, actual_string)

    #===========================================================================
    # Test Removing The and And
    #===========================================================================
    def test_sanitize_remove_and_and_the(self):
        the_and_and_string = "This IS And teST the"
        expected_no_the_or_and_string = 'this is test'
        actual_string = string_utils.sanitize_string(the_and_and_string, remove_the=True, remove_and=True)
        self.assertEqual(expected_no_the_or_and_string, actual_string)

    def test_sanitize_remove_and_and_the_adjacent(self):
        the_and_and_string = "ANd the This IS teST"
        expected_no_the_or_and_string = 'this is test'
        actual_string = string_utils.sanitize_string(the_and_and_string, remove_the=True, remove_and=True)
        self.assertEqual(expected_no_the_or_and_string, actual_string)
