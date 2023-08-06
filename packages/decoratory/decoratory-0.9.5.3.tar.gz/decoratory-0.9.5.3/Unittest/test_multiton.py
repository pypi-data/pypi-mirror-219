#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Test Multiton**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Test Multiton"
__module__ = "test_multiton.py"
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

from decoratory.multiton import Multiton


# -----------------------------------------------------------------------------
# Test Class
# noinspection PyPep8Naming
class TestMultiton(unittest.TestCase):
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
        """Unittest: Decoration without brackets
            --> No key: Multiton == Singleton
        """

        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(TestClass)

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # Multiton: b is a
        c = TestClassMultiton(name="b")  # Multiton: c is b is a

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIs(a, b)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_decoration_without_brackets_default_args(self):
        """Unittest: Decoration without brackets plus default args
            --> No key: Multiton == Singleton
        """
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(TestClass, "a")

        # Instances
        a = TestClassMultiton()  # New single default object a
        b = TestClassMultiton(name="b")  # Multiton: b is a
        c = TestClassMultiton(name="b")  # Multiton: c is b is a

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIs(a, b)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_decoration_without_brackets_default_kwargs(self):
        """Unittest: Decoration without brackets plus default kwargs
            --> No key: Multiton == Singleton
        """
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(TestClass, name="a")

        # Instances
        a = TestClassMultiton()  # New single object a
        b = TestClassMultiton(name="b")  # Multiton: b is a
        c = TestClassMultiton(name="b")  # Multiton: c is b is a

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIs(a, b)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_decoration_with_empty_brackets(self):
        """Unittest: Decoration with empty brackets
            --> No key: Multiton == Singleton
        """
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton()(TestClass)

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # Multiton: b is a
        c = TestClassMultiton(name="b")  # Multiton: c is b is a

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIs(a, b)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_decoration_with_invalid_parameter(self):
        """Unittest: Decoration with an invalid key object
            --> key = None: Multiton == Singleton
        """
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(key=list())(TestClass)  # mutable key!

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # Multiton: b is a
        c = TestClassMultiton(name="b")  # Multiton: c is b is a

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIs(a, b)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_decoration_with_object(self):
        """Unittest: Decoration with an object
            --> key = fixed: Multiton == Singleton
        """
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(key=tuple())(TestClass)  # immutable key!

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # Multiton: b is a
        c = TestClassMultiton(name="b")  # Multiton: c is b is a

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIs(a, b)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('a', None, 'any stuff')")
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_decoration_with_valid_parameter_id(self):
        """Unittest: Decoration with a valid key parameter: args[0]
            -> key = "name" attribute from args[0]
        """
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(key="{0}".format)(TestClass)  # args[0]

        # Instances
        a = TestClassMultiton("a")  # New single object a
        b = TestClassMultiton("b")  # New single object b
        c = TestClassMultiton("b")  # Multiton: c is b

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIsNot(a, b)
        self.assertIsNot(a, c)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('b', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('b', None, 'any stuff')")
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_decoration_with_valid_parameter_name(self):
        """Unittest: Decoration with a valid key parameter: kwargs['name']
            --> key = "name" attribute from kwargs['name']
        """
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(key="{name}".format)(
            TestClass)  # kwargs['name']

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # New single object b
        c = TestClassMultiton(name="b")  # Multiton: c is b

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIsNot(a, b)
        self.assertIsNot(a, c)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('b', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('b', None, 'any stuff')")
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_decoration_with_valid_parameter_inherited(self):
        """Unittest: Decoration with a valid key parameter: lambda name: name
            --> key = "name" attribute from lambda name: name
        """

        class TestClass(TestMultiton.TestClass):
            """Inherited test class"""
            pass

        TestClassMultiton = Multiton(key=lambda name: name)(TestClass)

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # New single object b
        c = TestClassMultiton(name="b")  # Multiton: c is b

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIsNot(a, b)
        self.assertIsNot(a, c)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('b', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('b', None, 'any stuff')")
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_decoration_with_callable_parameter(self):
        """Unittest: Decoration with a valid key callable: f = lambda name: name
            --> key = "name" attribute from function f = lambda name: name
        """
        f = lambda name: name  # Mapping as a function
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(key=f)(TestClass)

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # New single object b
        c = TestClassMultiton(name="b")  # Multiton: c is b

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIsNot(a, b)
        self.assertIsNot(a, c)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('b', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('b', None, 'any stuff')")
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_decoration_with_callable_classmethod(self):
        """Unittest: Decoration with a valid key callable (class method)
            --> key = "name" attribute from @classmethod key_function(cls, name)
        """

        class TestClass(TestMultiton.TestClass):
            """Test class"""

            @classmethod
            def key_function(cls, name):
                """Key callable"""
                return name

        TestClassMultiton = Multiton(key=TestClass.key_function)(TestClass)

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # New single object b
        c = TestClassMultiton(name="b")  # Multiton: c is b

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIsNot(a, b)
        self.assertIsNot(a, c)
        self.assertIs(b, c)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('b', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('b', None, 'any stuff')")
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(b, c)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)

    def test_sealed(self):
        """Unittest: Decoration with a valid key parameter: "name" attribute
            --> Method test for seal(), unseal() and issealed()
        """
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(key=lambda name: name)(TestClass)

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # New single object b
        c = TestClassMultiton(name="b")  # Multiton: c is b

        # Tests
        self.assertFalse(TestClassMultiton.issealed())
        TestClassMultiton.seal()
        self.assertTrue(TestClassMultiton.issealed())
        self.assertRaises(KeyError, TestClassMultiton, name="x")
        self.assertTrue(TestClassMultiton.issealed())
        TestClassMultiton.unseal()
        self.assertFalse(TestClassMultiton.issealed())
        d = TestClassMultiton(name="d")  # New single object d

        self.assertFalse(TestClassMultiton.issealed())
        TestClassMultiton.seal()  # Accessible because of sealed=False
        self.assertTrue(TestClassMultiton.issealed())
        self.assertRaises(KeyError, TestClassMultiton, name="y")
        self.assertTrue(TestClassMultiton.issealed())
        TestClassMultiton.unseal()  # Accessible via every multiton instance
        self.assertFalse(TestClassMultiton.issealed())
        e = TestClassMultiton(name="e")  # New single object e

        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIsInstance(d, TestClass)
        self.assertIsInstance(e, TestClass)
        self.assertIsNot(a, b)
        self.assertIsNot(a, c)
        self.assertIsNot(a, d)
        self.assertIsNot(a, e)
        self.assertIs(b, c)
        self.assertIsNot(b, d)
        self.assertIsNot(c, d)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('b', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('b', None, 'any stuff')")
        self.assertEqual(repr(d), "TestClass('d', None, 'any stuff')")
        self.assertEqual(repr(e), "TestClass('e', None, 'any stuff')")
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(a, e)
        self.assertEqual(b, c)
        self.assertNotEqual(b, d)
        self.assertNotEqual(c, d)
        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)
        self.assertEqual(TestClass.__doc__, d.__doc__)
        self.assertEqual(TestClass.__doc__, e.__doc__)

    def test_reset_instances(self):
        """Unittest: Decoration with a valid key parameter: "name" attribute
            --> Method test for instances and reset()
        """
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(key=lambda name: name,
                                     resettable=True)(TestClass)

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # New single object b

        # Tests
        self.assertDictEqual(TestClassMultiton.instances, {'a': a, 'b': b})
        TestClassMultiton.reset()
        self.assertDictEqual(TestClassMultiton.instances, {})
        self.assertFalse(TestClassMultiton.issealed())
        a = TestClassMultiton(name="a")  # New single object a
        self.assertDictEqual(TestClassMultiton.instances, {'a': a})
        TestClassMultiton.seal()
        self.assertTrue(TestClassMultiton.issealed())
        try:
            TestClassMultiton(name="b")
        except KeyError as ex:
            self.assertTupleEqual(ex.args, ('TestClass is sealed.', 'b'))
        self.assertDictEqual(TestClassMultiton.instances, {'a': a})
        TestClassMultiton.unseal()
        self.assertFalse(TestClassMultiton.issealed())
        c = TestClassMultiton(name="c")
        self.assertDictEqual(TestClassMultiton.instances, {'a': a, 'c': c})
        TestClassMultiton.instances.pop("a")
        self.assertDictEqual(TestClassMultiton.instances, {'c': c})
        TestClassMultiton.reset()
        self.assertDictEqual(TestClassMultiton.instances, {})

        TestClassMultiton.instances = {'a': a}
        self.assertDictEqual(TestClassMultiton.instances, {'a': a})
        a = TestClassMultiton(name="a")
        self.assertDictEqual(TestClassMultiton.instances, {'a': a})
        TestClassMultiton(name="a")
        self.assertDictEqual(TestClassMultiton.instances, {'a': a})

    def test_concurrency(self):
        """Unittest: Decoration with a valid key parameter: "name" attribute
            --> Two parallel multitons do not interfere with each other!
        """
        TestClass = TestMultiton.TestClass
        TestClassMultiton = Multiton(key=lambda name: name)(TestClass)
        AltClass = TestMultiton.AltClass
        AltClassMultiton = Multiton(key=lambda name: name)(AltClass)

        # Instances
        a = TestClassMultiton(name="a")  # New single object a
        b = TestClassMultiton(name="b")  # New single object b
        c = TestClassMultiton(name="b")  # Multiton: c is b
        x = AltClassMultiton(name="x")  # New single object x
        y = AltClassMultiton(name="y")  # New single object y
        z = AltClassMultiton(name="y")  # Multiton: z is y

        # Tests
        self.assertIsInstance(a, TestClass)
        self.assertIsInstance(b, TestClass)
        self.assertIsInstance(c, TestClass)
        self.assertIsNot(a, b)
        self.assertIsNot(a, c)
        self.assertIs(b, c)
        self.assertIsInstance(x, AltClass)
        self.assertIsInstance(y, AltClass)
        self.assertIsInstance(z, AltClass)
        self.assertIsNot(x, y)
        self.assertIsNot(x, z)
        self.assertIs(y, z)

        self.assertEqual(repr(a), "TestClass('a', None, 'any stuff')")
        self.assertEqual(repr(b), "TestClass('b', None, 'any stuff')")
        self.assertEqual(repr(c), "TestClass('b', None, 'any stuff')")
        self.assertEqual(repr(x), "AltClass('x', None, 'other stuff')")
        self.assertEqual(repr(y), "AltClass('y', None, 'other stuff')")
        self.assertEqual(repr(z), "AltClass('y', None, 'other stuff')")
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(b, c)
        self.assertNotEqual(x, y)
        self.assertNotEqual(x, z)
        self.assertEqual(y, z)

        self.assertEqual(TestClass.__doc__, TestClassMultiton.__doc__)
        self.assertEqual(TestClass.__doc__, a.__doc__)
        self.assertEqual(TestClass.__doc__, b.__doc__)
        self.assertEqual(TestClass.__doc__, c.__doc__)
        self.assertEqual(AltClass.__doc__, AltClassMultiton.__doc__)
        self.assertEqual(AltClass.__doc__, x.__doc__)
        self.assertEqual(AltClass.__doc__, y.__doc__)
        self.assertEqual(AltClass.__doc__, z.__doc__)


# -----------------------------------------------------------------------------
# Execution
if __name__ == "__main__":
    unittest.main()
