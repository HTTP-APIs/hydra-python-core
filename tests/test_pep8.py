"""Run PEP8 code format checker on all python files except samples directory."""

import os
from os.path import dirname, abspath, join
import unittest

import pep8


class Pep8Test(unittest.TestCase):
    def test_pep8(self):
        """Test method to check PEP8 compliance over the entire project."""
        self.file_structure = join(dirname(dirname(abspath(__file__))), "hydra_python_core")
        print("Testing for PEP8 compliance of python files in {}".format(
                self.file_structure))
        style = pep8.StyleGuide()
        style.options.max_line_length = 100  # Set this to desired maximum line length
        filenames = []
        # Set this to desired folder location
        for root, _, files in os.walk(self.file_structure):
            python_files = [f for f in files if f.endswith(".py")]
            for file in python_files:
                if len(root.split("samples")) != 2:  # Ignore samples directory
                    filename = "{0}/{1}".format(root, file)
                    filenames.append(filename)
        check = style.check_files(filenames)
        self.assertEqual(
            check.total_errors, 0, "PEP8 style errors: %d" % check.total_errors)


if __name__ == "__main__":
    print("Starting tests ..")
    unittest.main()
