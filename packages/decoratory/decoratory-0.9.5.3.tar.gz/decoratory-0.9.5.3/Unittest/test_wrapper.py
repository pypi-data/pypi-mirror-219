#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Test Wrapper**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Test Wrapper"
__module__ = "test_wrapper.py"
__author__ = "Martin Abel"
__maintainer__ = "Martin Abel"
__credits__ = ["Martin Abel"]
__company__ = "eVation"
__email__ = "python@evation.eu"
__url__ = "http://evation.eu"
__copyright__ = f"(c) copyright 2020-2023, {__author__}, {__company__}"
__created__ = "2020-01-01"
__version__ = "0.9.5.1"
__date__ = "2023-07-17"
__time__ = "15:43:02"
__state__ = "Beta"
__license__ = "MIT"

# -----------------------------------------------------------------------------
# Libraries & Modules
import unittest

from decoratory.wrapper import Wrapper
from decoratory.basic import F


# -----------------------------------------------------------------------------
# Test Class
# noinspection PyPep8Naming
class TestWrapper(unittest.TestCase):

    def setUp(self):
        """Preparation"""
        pass

    def tearDown(self):
        """Wrap-up"""
        pass

    def test_decoration_customized(self):
        """Unittest: Wrapper with customized default text, only"""

        # Result list
        res = list()

        def printer(txt: str = "Default text"):
            """The default printer"""
            res.append(f"{printer.__name__}: '{txt}'")

        wrp_printer = Wrapper(printer, "Customized text")

        # ---------------------------------------------------------------------
        # Checks
        self.assertTrue(isinstance(wrp_printer, Wrapper))

        # Call
        res.clear()
        wrp_printer()
        self.assertListEqual(res, ["printer: 'Customized text'"])

        wrp_printer = Wrapper(printer, txt="Customized phrase")

        res.clear()
        wrp_printer()
        self.assertListEqual(res, ["printer: 'Customized phrase'"])

    def test_decoration_nobrackets(self):
        """Unittest: Wrapper without brackets"""

        # Result list
        res = list()

        @Wrapper
        def printer(txt: str = "Default text"):
            """The default printer"""
            res.append(f"{printer.__name__}: '{txt}'")

        # ---------------------------------------------------------------------
        # Checks
        self.assertTrue(isinstance(printer, Wrapper))

        # Call
        res.clear()
        printer()
        self.assertListEqual(res, ["printer: 'Default text'"])

    def test_decoration_empty_brackets(self):
        """Unittest: Wrapper with empty brackets"""

        # Result list
        res = list()

        @Wrapper()
        def printer(txt: str = "Default text"):
            """The default printer"""
            res.append(f"{printer.__name__}: '{txt}'")

        # ---------------------------------------------------------------------
        # Checks
        self.assertTrue(isinstance(printer, Wrapper))

        # Call
        res.clear()
        printer()
        self.assertListEqual(res, ["printer: 'Default text'"])

    def test_decoration_before_after(self):
        """Unittest: Wrapper with before and after activities"""

        # Result list
        res = list()

        def before_printer(txt: str = "BEFORE"):
            """The before printer"""
            res.append(f"{before_printer.__name__}: '{txt}'")

        def after_printer(txt: str = "AFTER"):
            """The after printer"""
            res.append(f"{after_printer.__name__}: '{txt}'")

        @Wrapper(before=before_printer, after=after_printer)
        def printer(txt: str = "Default text"):
            """The default printer"""
            res.append(f"{printer.__name__}: '{txt}'")

        # ---------------------------------------------------------------------
        # Checks
        self.assertTrue(isinstance(printer, Wrapper))

        # Call
        res.clear()
        printer()
        self.assertListEqual(res, ["before_printer: 'BEFORE'",
                                   "printer: 'Default text'",
                                   "after_printer: 'AFTER'"])

    def test_decoration_replace(self):
        """Unittest: Wrapper with replace activity"""

        # Result list
        res = list()

        def replace_printer(txt: str = "REPLACE"):
            """The replace printer"""
            res.append(f"{replace_printer.__name__}: '{txt}'")

        @Wrapper(replace=replace_printer)
        def printer(txt: str = "Default text"):
            """The default printer"""
            res.append(f"{printer.__name__}: '{txt}'")

        # ---------------------------------------------------------------------
        # Checks
        self.assertTrue(isinstance(printer, Wrapper))

        # Call
        res.clear()
        printer()
        self.assertListEqual(res, ["replace_printer: 'REPLACE'"])

    def test_decoration_replace_wrapper(self):
        """Unittest: Wrapper with replace wrapper"""

        # Result list
        res = list()

        def replace_wrapper(value: str = "replace"):
            """The replace wrapper"""
            # 1. Edit the call parameters for the original functionality
            value = value.upper()
            # 2. Execute original functionality with modified call parameters
            result = printer.substitute.callee(value)  # (1)
            # 3. Edit the result and return this modified result
            return f"result: '{result}'"

        @Wrapper(replace=replace_wrapper)
        def printer(txt: str = "Default text"):
            """The default printer"""
            res.append(f"{printer.__name__}: '{txt}'")
            return txt

        # ---------------------------------------------------------------------
        # Checks
        self.assertTrue(isinstance(printer, Wrapper))

        # Call
        res.clear()
        res.append(printer())
        self.assertListEqual(res, ["printer: 'REPLACE'",
                                   "result: 'REPLACE'"])

    def test_decoration_before_after_lists(self):
        """Unittest: Wrapper with list of before and after activities"""

        # Result list
        res = list()

        def before_printer(txt: str = "Before text"):
            """The before printer"""
            res.append(f"{before_printer.__name__:14s}: '{txt}'")

        def after_printer(txt: str = "After text"):
            """The after printer"""
            res.append(f"{after_printer.__name__:14s}: '{txt}'")

        @Wrapper(before=[F(before_printer, "Text01"),
                         F(before_printer, txt="Text02"),
                         before_printer],
                 after=[after_printer,
                        F(after_printer, "Text01"),
                        F(after_printer, txt="Text02")])
        def printer(txt: str = "Default text"):
            """The default printer"""
            res.append(f"{printer.__name__:14s}: '{txt}'")

        # ---------------------------------------------------------------------
        # Checks
        self.assertTrue(isinstance(printer, Wrapper))

        # Call
        res.clear()
        printer()
        self.assertListEqual(res, ["before_printer: 'Text01'",
                                   "before_printer: 'Text02'",
                                   "before_printer: 'Before text'",
                                   "printer       : 'Default text'",
                                   "after_printer : 'After text'",
                                   "after_printer : 'Text01'",
                                   "after_printer : 'Text02'"])

    def test_decoration_before_replace_after_lists(self):
        """Unittest: Wrapper with list of before, after and replace activities"""

        # Result list
        res = list()

        def before_printer(txt: str = "Before text"):
            """The before printer"""
            res.append(f"{before_printer.__name__:15s}: '{txt}'")

        def after_printer(txt: str = "After text"):
            """The after printer"""
            res.append(f"{after_printer.__name__:15s}: '{txt}'")

        def replace_printer(add: int = 1, *, result=None):
            """The replace printer"""
            result = add + result if isinstance(result, int) else 0
            res.append(f"{replace_printer.__name__:15s}: result = {result}")
            return result

        @Wrapper(before=[F(before_printer, "First text"),
                         before_printer],
                 after=[after_printer,
                        F(after_printer, "Last text")],
                 replace=[F(replace_printer, 1, result=0),
                          F(replace_printer, 2),
                          F(replace_printer, 3),
                          F(replace_printer, 4)])
        def printer(txt: str = "Default text"):
            """The default printer"""
            res.append(f"{printer.__name__:14s}: '{txt}'")

        # ---------------------------------------------------------------------
        # Checks
        self.assertTrue(isinstance(printer, Wrapper))

        # Call
        res.clear()
        printer()
        self.assertListEqual(res, ["before_printer : 'First text'",
                                   "before_printer : 'Before text'",
                                   "replace_printer: result = 1",
                                   "replace_printer: result = 3",
                                   "replace_printer: result = 6",
                                   "replace_printer: result = 10",
                                   "after_printer  : 'After text'",
                                   "after_printer  : 'Last text'"])


# -----------------------------------------------------------------------------
# Execution
if __name__ == "__main__":
    unittest.main()
