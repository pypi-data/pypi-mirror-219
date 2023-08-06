#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Test Singleton**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Test Singleton"
__module__ = "test_singleton.py"
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

from decoratory.singleton import Singleton, SemiSingleton


# -----------------------------------------------------------------------------
# Test Class
# noinspection PyPep8Naming
class TestSingleton(unittest.TestCase):
    class TestClass:
        """A simple test class with some parameters"""

        def __init__(self, name: str, foo=None, bar="any stuff"):
            self.name = name
            self.foo = foo
            self.bar = bar

        def __repr__(self):
            return f"{self.__class__.__name__}(" \
                   f"'{self.name}', {self.foo}, '{self.bar}')"

    class AltClass:
        """An alternative test class with some parameters"""

        def __init__(self, name: str, foo=None, bar="other stuff"):
            self.name = name
            self.foo = foo
            self.bar = bar

        def __repr__(self):
            return f"{self.__class__.__name__}(" \
                   f"'{self.name}', {self.foo}, '{self.bar}')"

    def setUp(self):
        """Setup"""
        pass

    def tearDown(self):
        """Shutdown"""
        pass

    def test_decoration_without_brackets(self):
        """Unittest: Decoration without brackets"""

        TestClass = TestSingleton.TestClass
        TestClassSingleton = Singleton(TestClass)

        # Instances
        a = TestClassSingleton(name="a")  # New single object a
        b = TestClassSingleton(name="b")  # Singleton: b is a

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIs(a, b)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertEqual(TestClass.__doc__, TestClassSingleton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)

    def test_decoration_with_empty_brackets(self):
        """Unittest: Decoration with empty brackets"""

        TestClass = TestSingleton.TestClass
        TestClassSingleton = Singleton()(TestClass)

        # Instances
        a = TestClassSingleton(name="a")  # New single object a
        b = TestClassSingleton(name="b")  # Singleton: b is a

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIs(a, b)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertEqual(TestClass.__doc__, TestClassSingleton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)

    def test_decoration_with_default(self):
        """Unittest: Decoration with default"""

        TestClass = TestSingleton.TestClass
        TestClassSingleton = Singleton(TestClass, name="a")

        # Instances
        a = TestClassSingleton()  # New single object a (default)
        b = TestClassSingleton(name="b")  # Singleton: b is a

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIs(a, b)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertEqual(TestClass.__doc__, TestClassSingleton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)

    def test_decoration_with_resettable(self):
        """Unittest: Decoration with resettable"""

        # ---------------------------------------------------------------------
        # Default: resettable = False
        TestClass = TestSingleton.TestClass
        TestClassSingleton = Singleton(TestClass)

        # Instances
        a = TestClassSingleton(name="a")  # New single object a (default)

        # Tests
        self.assertFalse(hasattr(TestClass, "reset"))
        self.assertFalse(hasattr(TestClassSingleton, "reset"))
        self.assertFalse(hasattr(a, "reset"))

        # Test exception
        try:
            TestClassSingleton.reset()
        except AttributeError:
            pass
        else:
            raise AssertionError

        # ---------------------------------------------------------------------
        # Set: resettable = False
        TestClass = TestSingleton.TestClass
        # noinspection PyArgumentEqualDefault
        TestClassSingleton = Singleton(TestClass, resettable=False)

        # Instances
        a = TestClassSingleton(name="a")  # New single object a (default)

        # Tests
        self.assertFalse(hasattr(TestClass, "reset"))
        self.assertFalse(hasattr(TestClassSingleton, "reset"))
        self.assertFalse(hasattr(a, "reset"))

        # Test exception
        try:
            TestClassSingleton.reset()
        except AttributeError:
            pass
        else:
            raise AssertionError

        # ---------------------------------------------------------------------
        # Set: resettable = True
        TestClass = TestSingleton.TestClass
        TestClassSingleton = Singleton(TestClass, resettable=True)

        # Instances
        a = TestClassSingleton(name="a")  # New single object a (default)

        # Tests
        self.assertFalse(hasattr(TestClass, "reset"))
        self.assertTrue(hasattr(TestClassSingleton, "reset"))  # The only one!
        self.assertFalse(hasattr(a, "reset"))

        b = TestClassSingleton(name="b")  # Singleton: b is a
        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertIs(a, b)

        TestClassSingleton.reset()

        c = TestClassSingleton(name="c")  # New single object c (default)
        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('c', None, 'any stuff')")
        self.assertNotEqual(a, c)
        self.assertIsNot(a, c)

    def test_semi_singleton(self):
        """Unittest: Decoration as a semi singleton"""

        TestClass = TestSingleton.TestClass
        TestClassSingleton = SemiSingleton(TestClass)

        # Instances
        a = TestClassSingleton(name="a")  # New single object a (default)

        # Tests
        self.assertFalse(hasattr(TestClass, "reset"))
        self.assertTrue(hasattr(TestClassSingleton, "reset"))  # The only one!
        self.assertFalse(hasattr(a, "reset"))

        b = TestClassSingleton(name="b")  # Singleton: b is a
        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertIs(a, b)

        TestClassSingleton.reset()

        c = TestClassSingleton(name="c")  # New single object c (default)
        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('c', None, 'any stuff')")
        self.assertNotEqual(a, c)
        self.assertIsNot(a, c)

    def test_get_instance(self):
        """Unittest: Decoration get_instance"""

        TestClass = TestSingleton.TestClass
        TestClassSingleton = Singleton(TestClass)

        # Instance
        a = TestClassSingleton(name="a")  # New single object a (default)

        # Tests
        self.assertFalse(hasattr(TestClass, "get_instance"))
        self.assertTrue(hasattr(TestClassSingleton, "get_instance"))  # This!
        self.assertFalse(hasattr(a, "get_instance"))

        self.assertIs(TestClassSingleton.get_instance(), a)
        self.assertEqual(TestClassSingleton.get_instance(), a)

    def test_concurrency(self):
        """Unittest: Decoration concurrency
            --> Two parallel singletons do not interfere with each other!
        """

        TestClass = TestSingleton.TestClass
        TestClassSingleton = Singleton(TestClass)
        AltClass = TestSingleton.AltClass
        AltClassSingleton = Singleton()(AltClass)

        # Instances
        a = TestClassSingleton(name="a")  # New single object a
        b = TestClassSingleton(name="b")  # Singleton: b is a
        c = AltClassSingleton(name="c")  # New single object c
        d = AltClassSingleton(name="d")  # Singleton: d is c

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, AltClass)
        self.assertIsInstance(d, AltClass)
        self.assertIs(a, b)
        self.assertIs(c, d)
        self.assertIsNot(a, c)
        self.assertIsNot(a, d)
        self.assertIsNot(b, c)
        self.assertIsNot(b, d)

        self.assertEqual(a, b)
        self.assertEqual(c, d)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(b, c)
        self.assertNotEqual(b, d)

        self.assertEqual(TestClass.__doc__, TestClassSingleton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(AltClass.__doc__, AltClassSingleton.__doc__)
        self.assertEqual(AltClass.__doc__, c.__doc__)
        self.assertEqual(AltClass.__doc__, d.__doc__)


# -----------------------------------------------------------------------------
# Execution
if __name__ == "__main__":
    unittest.main()
