#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Test_Basic**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Test_Basic"
__module__ = "test_basic.py"
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

from decoratory.basic import (Activation, F, Parser, X, BaseDecorator)


# -----------------------------------------------------------------------------
# Test functions
def cmp(f: F, t: tuple):
    """Compare F with tuple"""
    return (x == y for x, y in zip(f, t))


# -----------------------------------------------------------------------------
# Test Class
# noinspection PyPep8Naming,PyArgumentEqualDefault
class TestDecotools(unittest.TestCase):

    def setUp(self):
        """Preparation"""
        pass

    def tearDown(self):
        """Wrap-up"""
        pass

    def test_activation(self):
        """Unittest: Activation"""

        # ---------------------------------------------------------------------
        # Test
        self.assertEqual(len(Activation), 4)

        self.assertNotEqual(Activation.NONE, Activation.BEFORE)
        self.assertNotEqual(Activation.NONE, Activation.AFTER)
        self.assertNotEqual(Activation.NONE, Activation.BEFORE_AND_AFTER)
        self.assertNotEqual(Activation.BEFORE, Activation.AFTER)
        self.assertNotEqual(Activation.BEFORE, Activation.BEFORE_AND_AFTER)
        self.assertNotEqual(Activation.AFTER, Activation.BEFORE_AND_AFTER)

        self.assertEqual(Activation.BEFORE_AND_AFTER,
                         Activation.BEFORE | Activation.AFTER)

    def test_F(self):
        """Unittest: F wrapper"""

        # A callable
        def function(x, y):
            """Test function"""
            return x + y

        # ---------------------------------------------------------------------
        # Test

        # Callee is mandatory
        try:
            # noinspection PyArgumentList
            F()
        except TypeError:
            pass
        else:
            raise AssertionError

        # Empty parameters
        self.assertTrue(cmp(F(function), (function, (), {})))
        self.assertTrue(cmp(F('function'), ('function', (), {})))

        # Positional and keyword parameters
        self.assertTrue(cmp(F(function, 2, 3),
                            (function, (2, 3), {})))
        self.assertTrue(cmp(F(function, x=2, y=3),
                            (function, (), {'x': 2, 'y': 3})))
        self.assertTrue(cmp(F(function, 2, y=3),
                            (function, (2,), {'y': 3})))

        # repr()
        self.assertEqual(repr(F(function)),
                         f"F({function.__name__})")
        self.assertEqual(repr(F(function, 2, 3)),
                         f"F({function.__name__}, 2, 3)")
        self.assertEqual(repr(F(function, 2, y=3)),
                         f"F({function.__name__}, 2, y=3)")
        self.assertEqual(repr(F(function, x=2, y=3)),
                         f"F({function.__name__}, x=2, y=3)")
        self.assertEqual(repr(F(function, '2', '3')),
                         f'F({function.__name__}, "2", "3")')
        self.assertEqual(repr(F(function, '2', y='3')),
                         f'F({function.__name__}, "2", y="3")')
        self.assertEqual(repr(F(function, x='2', y='3')),
                         f'F({function.__name__}, x="2", y="3")')

        self.assertEqual(repr(F('function')),
                         f'F("function")')
        self.assertEqual(repr(F('function', 2, 3)),
                         f'F("function", 2, 3)')
        self.assertEqual(repr(F('function', 2, y=3)),
                         f'F("function", 2, y=3)')
        self.assertEqual(repr(F('function', x=2, y=3)),
                         f'F("function", x=2, y=3)')
        self.assertEqual(repr(F('function', '2', '3')),
                         f'F("function", "2", "3")')
        self.assertEqual(repr(F('function', '2', y='3')),
                         f'F("function", "2", y="3")')
        self.assertEqual(repr(F('function', x='2', y='3')),
                         f'F("function", x="2", y="3")')

        # str()
        self.assertEqual(str(F(function)),
                         f"{function.__name__}()")
        self.assertEqual(str(F(function, 2, 3)),
                         f"{function.__name__}(2, 3)")
        self.assertEqual(str(F(function, 2, y=3)),
                         f"{function.__name__}(2, y=3)")
        self.assertEqual(str(F(function, x=2, y=3)),
                         f"{function.__name__}(x=2, y=3)")
        self.assertEqual(str(F(function, '2', '3')),
                         f'{function.__name__}("2", "3")')
        self.assertEqual(str(F(function, '2', y='3')),
                         f'{function.__name__}("2", y="3")')
        self.assertEqual(str(F(function, x='2', y='3')),
                         f'{function.__name__}(x="2", y="3")')

        self.assertEqual(str(F('function')),
                         f'function()')
        self.assertEqual(str(F('function', 2, 3)),
                         f'function(2, 3)')
        self.assertEqual(str(F('function', 2, y=3)),
                         f'function(2, y=3)')
        self.assertEqual(str(F('function', x=2, y=3)),
                         f'function(x=2, y=3)')
        self.assertEqual(str(F('function', "2", "3")),
                         f'function("2", "3")')
        self.assertEqual(str(F('function', "2", y="3")),
                         f'function("2", y="3")')
        self.assertEqual(str(F('function', x="2", y="3")),
                         f'function(x="2", y="3")')

        # hash()
        self.assertEqual(hash(F(function)), hash(function))
        self.assertEqual(hash(F(function, 2, 3)), hash(function))
        self.assertEqual(hash(F(function, 2, y=3)), hash(function))
        self.assertEqual(hash(F(function, x=2, y=3)), hash(function))

        self.assertEqual(hash(F('function')), hash('function'))
        self.assertEqual(hash(F('function', 2, 3)), hash('function'))
        self.assertEqual(hash(F('function', 2, y=3)), hash('function'))
        self.assertEqual(hash(F('function', x=2, y=3)), hash('function'))

        self.assertNotEqual(hash(F('function')), hash(function))
        self.assertNotEqual(hash(F('function', 2, 3)), hash(function))
        self.assertNotEqual(hash(F('function', 2, y=3)), hash(function))
        self.assertNotEqual(hash(F('function', x=2, y=3)), hash(function))

        self.assertNotEqual(hash(F(function)), hash('function'))
        self.assertNotEqual(hash(F(function, 2, 3)), hash('function'))
        self.assertNotEqual(hash(F(function, 2, y=3)), hash('function'))
        self.assertNotEqual(hash(F(function, x=2, y=3)), hash('function'))

        # eq()
        self.assertTrue(F(function) == F(function))
        self.assertTrue(F(function) == function)
        self.assertFalse(F('function') == function)
        self.assertFalse(F(function) == 'function')
        self.assertFalse(F(function) == 13)

        # iter()
        itr = iter(F(function, 2, y=3))
        self.assertEqual(next(itr), function)
        self.assertEqual(next(itr), (2,))
        self.assertEqual(next(itr), {'y': 3})

        # eval()
        self.assertEqual(F(function, 2, 3).eval(), 5)
        self.assertEqual(F(function, 2, y=3).eval(), 5)
        self.assertEqual(F(function, x=2, y=3).eval(), 5)

        class A:
            """Test class"""

            @staticmethod
            def stc_method(x, y):
                """Static method"""
                return x + y

        self.assertEqual(F(A.stc_method, 2, 3).eval(), 5)
        self.assertEqual(F(A.stc_method, 2, y=3).eval(), 5)
        self.assertEqual(F(A.stc_method, x=2, y=3).eval(), 5)

        self.assertEqual(F('stc_method', A, 2, 3).eval(), 5)
        self.assertEqual(F('stc_method', A, 2, y=3).eval(), 5)
        self.assertEqual(F('stc_method', A, x=2, y=3).eval(), 5)

        self.assertEqual(F('stc_method', 2, 3).eval(obj=A), 5)
        self.assertEqual(F('stc_method', 2, y=3).eval(obj=A), 5)
        self.assertEqual(F('stc_method', x=2, y=3).eval(obj=A), 5)

        class A:
            """Test class"""

            @classmethod
            def cls_method(cls, x, y):
                """Class method"""
                return x + y

        self.assertEqual(F(A.cls_method, 2, 3).eval(), 5)
        self.assertEqual(F(A.cls_method, 2, y=3).eval(), 5)
        self.assertEqual(F(A.cls_method, x=2, y=3).eval(), 5)

        self.assertEqual(F('cls_method', A, 2, 3).eval(), 5)
        self.assertEqual(F('cls_method', A, 2, y=3).eval(), 5)
        self.assertEqual(F('cls_method', A, x=2, y=3).eval(), 5)

        self.assertEqual(F('cls_method', 2, 3).eval(obj=A), 5)
        self.assertEqual(F('cls_method', 2, y=3).eval(obj=A), 5)
        self.assertEqual(F('cls_method', x=2, y=3).eval(obj=A), 5)

        class A:
            """Test class"""

            def __init__(self, x=2):
                self.x = x

            def obj_method(self, y):
                """Instance method"""
                return self.x + y

        self.assertEqual(F(A(2).obj_method, 3).eval(), 5)
        self.assertEqual(F(A(2).obj_method, y=3).eval(), 5)
        self.assertEqual(F(A(x=2).obj_method, 3).eval(), 5)
        self.assertEqual(F(A(x=2).obj_method, y=3).eval(), 5)

        self.assertEqual(F('obj_method', A(2), 3).eval(), 5)
        self.assertEqual(F('obj_method', A(2), y=3).eval(), 5)
        self.assertEqual(F('obj_method', A(x=2), 3).eval(), 5)
        self.assertEqual(F('obj_method', A(x=2), y=3).eval(), 5)

        self.assertEqual(F('obj_method', 3).eval(obj=A(2)), 5)
        self.assertEqual(F('obj_method', y=3).eval(obj=A(2)), 5)
        self.assertEqual(F('obj_method', 3).eval(obj=A(x=2)), 5)
        self.assertEqual(F('obj_method', y=3).eval(obj=A(x=2)), 5)

        class A:
            """Test class"""

            def __init__(self, x=2):
                self.x = x

            def __call__(self, y):
                return self.x + y

        self.assertEqual(F(A(2), 3).eval(), 5)
        self.assertEqual(F(A(2), y=3).eval(), 5)
        self.assertEqual(F(A(x=2), 3).eval(), 5)
        self.assertEqual(F(A(x=2), y=3).eval(), 5)

        # Setter
        f = F(function)
        try:
            # noinspection PyPropertyAccess
            f.callee = function
        except AttributeError:
            pass
        else:
            raise AttributeError

        f.callee_args = (2, 3, 4)
        self.assertTupleEqual(f.callee_args, (2, 3, 4))
        f.callee_kwargs = {'x': 2, 'y': 3, 'z': 4}
        self.assertDictEqual(f.callee_kwargs, {'x': 2, 'y': 3, 'z': 4})

    def test_X(self):
        """Unittest: X wrapper"""

        # A callable
        def function(x, y):
            """Test function"""
            return int(x) + int(y)

        # ---------------------------------------------------------------------
        # Test

        # Callee is mandatory
        try:
            # noinspection PyArgumentList
            X()
        except TypeError:
            pass
        else:
            raise AssertionError

        # Empty parameters
        self.assertTrue(cmp(X(function), (function, (), {})))
        self.assertTrue(cmp(X('function'), ('function', (), {})))

        # Positional and keyword parameters
        self.assertTrue(cmp(X(function, 2, 3),
                            (function, (2, 3), {})))
        self.assertTrue(cmp(X(function, x=2, y=3),
                            (function, (), {'x': 2, 'y': 3})))
        self.assertTrue(cmp(X(function, 2, y=3),
                            (function, (2,), {'y': 3})))

        # repr()
        self.assertEqual(repr(X(function)),
                         f"X({function.__name__})")
        self.assertEqual(repr(X(function, 2, 3)),
                         f"X({function.__name__}, 2, 3)")
        self.assertEqual(repr(X(function, 2, y=3)),
                         f"X({function.__name__}, 2, y=3)")
        self.assertEqual(repr(X(function, x=2, y=3)),
                         f"X({function.__name__}, x=2, y=3)")
        self.assertEqual(repr(X(function, '2', '3')),
                         f'X({function.__name__}, "2", "3")')
        self.assertEqual(repr(X(function, '2', y='3')),
                         f'X({function.__name__}, "2", y="3")')
        self.assertEqual(repr(X(function, x='2', y='3')),
                         f'X({function.__name__}, x="2", y="3")')

        self.assertEqual(repr(X('function')),
                         f'X("function")')
        self.assertEqual(repr(X('function', 2, 3)),
                         f'X("function", 2, 3)')
        self.assertEqual(repr(X('function', 2, y=3)),
                         f'X("function", 2, y=3)')
        self.assertEqual(repr(X('function', x=2, y=3)),
                         f'X("function", x=2, y=3)')
        self.assertEqual(repr(X('function', '2', '3')),
                         f'X("function", "2", "3")')
        self.assertEqual(repr(X('function', '2', y='3')),
                         f'X("function", "2", y="3")')
        self.assertEqual(repr(X('function', x='2', y='3')),
                         f'X("function", x="2", y="3")')

        # str()
        self.assertEqual(str(X(function)),
                         f"{function.__name__}()")
        self.assertEqual(str(X(function, 2, 3)),
                         f"{function.__name__}(2, 3)")
        self.assertEqual(str(X(function, 2, y=3)),
                         f"{function.__name__}(2, y=3)")
        self.assertEqual(str(X(function, x=2, y=3)),
                         f"{function.__name__}(x=2, y=3)")
        self.assertEqual(str(X(function, '2', '3')),
                         f'{function.__name__}("2", "3")')
        self.assertEqual(str(X(function, '2', y='3')),
                         f'{function.__name__}("2", y="3")')
        self.assertEqual(str(X(function, x='2', y='3')),
                         f'{function.__name__}(x="2", y="3")')

        self.assertEqual(str(X('function')),
                         f'function()')
        self.assertEqual(str(X('function', 2, 3)),
                         f'function(2, 3)')
        self.assertEqual(str(X('function', 2, y=3)),
                         f'function(2, y=3)')
        self.assertEqual(str(X('function', x=2, y=3)),
                         f'function(x=2, y=3)')
        self.assertEqual(str(X('function', "2", "3")),
                         f'function("2", "3")')
        self.assertEqual(str(X('function', "2", y="3")),
                         f'function("2", y="3")')
        self.assertEqual(str(X('function', x="2", y="3")),
                         f'function(x="2", y="3")')

        # hash()
        self.assertEqual(hash(X(function)), hash(function))
        self.assertEqual(hash(X(function, 2, 3)), hash(function))
        self.assertEqual(hash(X(function, 2, y=3)), hash(function))
        self.assertEqual(hash(X(function, x=2, y=3)), hash(function))

        self.assertEqual(hash(X('function')), hash('function'))
        self.assertEqual(hash(X('function', 2, 3)), hash('function'))
        self.assertEqual(hash(X('function', 2, y=3)), hash('function'))
        self.assertEqual(hash(X('function', x=2, y=3)), hash('function'))

        self.assertNotEqual(hash(X('function')), hash(function))
        self.assertNotEqual(hash(X('function', 2, 3)), hash(function))
        self.assertNotEqual(hash(X('function', 2, y=3)), hash(function))
        self.assertNotEqual(hash(X('function', x=2, y=3)), hash(function))

        self.assertNotEqual(hash(X(function)), hash('function'))
        self.assertNotEqual(hash(X(function, 2, 3)), hash('function'))
        self.assertNotEqual(hash(X(function, 2, y=3)), hash('function'))
        self.assertNotEqual(hash(X(function, x=2, y=3)), hash('function'))

        # eq()
        self.assertTrue(X(function) == X(function))
        self.assertTrue(X(function) == function)
        self.assertFalse(X('function') == function)
        self.assertFalse(X(function) == 'function')
        self.assertFalse(X(function) == 13)

        # iter()
        itr = iter(X(function, 2, y=3))
        self.assertEqual(next(itr), function)
        self.assertEqual(next(itr), (2,))
        self.assertEqual(next(itr), {'y': 3})

        # eval()
        self.assertEqual(X(function, 2, 3).eval(), 5)
        self.assertEqual(X(function, 2, y=3).eval(), 5)
        self.assertEqual(X(function, x=2, y=3).eval(), 5)

        class A:
            """Test class"""

            @staticmethod
            def stc_method(x, y):
                """Static method"""
                return x + y

        self.assertEqual(X(A.stc_method, 2, 3).eval(), 5)
        self.assertEqual(X(A.stc_method, 2, y=3).eval(), 5)
        self.assertEqual(X(A.stc_method, x=2, y=3).eval(), 5)

        self.assertEqual(X('stc_method', A, 2, 3).eval(), 5)
        self.assertEqual(X('stc_method', A, 2, y=3).eval(), 5)
        self.assertEqual(X('stc_method', A, x=2, y=3).eval(), 5)

        self.assertEqual(X('stc_method', 2, 3).eval(obj=A), 5)
        self.assertEqual(X('stc_method', 2, y=3).eval(obj=A), 5)
        self.assertEqual(X('stc_method', x=2, y=3).eval(obj=A), 5)

        class A:
            """Test class"""

            @classmethod
            def cls_method(cls, x, y):
                """Class method"""
                return x + y

        self.assertEqual(X(A.cls_method, 2, 3).eval(), 5)
        self.assertEqual(X(A.cls_method, 2, y=3).eval(), 5)
        self.assertEqual(X(A.cls_method, x=2, y=3).eval(), 5)

        self.assertEqual(X('cls_method', A, 2, 3).eval(), 5)
        self.assertEqual(X('cls_method', A, 2, y=3).eval(), 5)
        self.assertEqual(X('cls_method', A, x=2, y=3).eval(), 5)

        self.assertEqual(X('cls_method', 2, 3).eval(obj=A), 5)
        self.assertEqual(X('cls_method', 2, y=3).eval(obj=A), 5)
        self.assertEqual(X('cls_method', x=2, y=3).eval(obj=A), 5)

        class A:
            """Test class"""

            def __init__(self, x=2):
                self.x = x

            def obj_method(self, y):
                """Instance method"""
                return self.x + y

        self.assertEqual(X(A(2).obj_method, 3).eval(), 5)
        self.assertEqual(X(A(2).obj_method, y=3).eval(), 5)
        self.assertEqual(X(A(x=2).obj_method, 3).eval(), 5)
        self.assertEqual(X(A(x=2).obj_method, y=3).eval(), 5)

        self.assertEqual(X('obj_method', A(2), 3).eval(), 5)
        self.assertEqual(X('obj_method', A(2), y=3).eval(), 5)
        self.assertEqual(X('obj_method', A(x=2), 3).eval(), 5)
        self.assertEqual(X('obj_method', A(x=2), y=3).eval(), 5)

        self.assertEqual(X('obj_method', 3).eval(obj=A(2)), 5)
        self.assertEqual(X('obj_method', y=3).eval(obj=A(2)), 5)
        self.assertEqual(X('obj_method', 3).eval(obj=A(x=2)), 5)
        self.assertEqual(X('obj_method', y=3).eval(obj=A(x=2)), 5)

        class A:
            """Test class"""

            def __init__(self, x=2):
                self.x = x

            def __call__(self, y):
                return self.x + y

        self.assertEqual(X(A(2), 3).eval(), 5)
        self.assertEqual(X(A(2), y=3).eval(), 5)
        self.assertEqual(X(A(x=2), 3).eval(), 5)
        self.assertEqual(X(A(x=2), y=3).eval(), 5)

        # Setter
        x = X(function)
        try:
            # noinspection PyPropertyAccess
            x.callee = function
        except AttributeError:
            pass
        else:
            raise AttributeError

        x.callee_args = (2, 3, 4)
        self.assertTupleEqual(x.callee_args, (2, 3, 4))
        x.callee_kwargs = {'x': 2, 'y': 3, 'z': 4}
        self.assertDictEqual(x.callee_kwargs, {'x': 2, 'y': 3, 'z': 4})

    def test_Parser(self):
        """Unittest: Parser"""

        # A callable
        def function(x, y):
            """Test function"""
            return x + y

        # ---------------------------------------------------------------------
        # Unittest: Parser.tuple

        # Callee is mandatory
        try:
            Parser.tuple(tuple())
        except TypeError:
            pass
        else:
            raise AssertionError

        # No args, no kwargs
        self.assertTrue(cmp(Parser.tuple((function,)), (function, (), {})))
        self.assertTrue(cmp(Parser.tuple(('function',)), ('function', (), {})))
        try:
            Parser.tuple((123456,))
        except TypeError:
            pass
        else:
            # noinspection PyStatementEffect
            AssertionError

        # Only args
        self.assertTrue(cmp(Parser.tuple((function, (2, 3))),
                            (function, (2, 3), {})))
        self.assertTrue(cmp(Parser.tuple(('function', (2, 3))),
                            ('function', (2, 3), {})))

        # Only kwargs
        self.assertTrue(cmp(Parser.tuple((function, {'x': 2, 'y': 3})),
                            (function, (), {'x': 2, 'y': 3})))
        self.assertTrue(cmp(Parser.tuple(('function', {'x': 2, 'y': 3})),
                            ('function', (), {'x': 2, 'y': 3})))

        # args and kwargs
        self.assertTrue(cmp(Parser.tuple((function, (2,), {'y': 3})),
                            (function, (2,), {'y': 3})))
        self.assertTrue(cmp(Parser.tuple(('function', (2,), {'y': 3})),
                            ('function', (2,), {'y': 3})))

        # ---------------------------------------------------------------------
        # Unittest: Parser.list
        self.assertListEqual(Parser.list([F('a'), F('b'), F('c')]),
                             [F('a'), F('b'), F('c')])
        self.assertListEqual(Parser.list([function, function, function]),
                             [F(function), F(function), F(function)])
        self.assertListEqual(Parser.list(['a', 'b', 'c']),
                             [F('a'), F('b'), F('c')])
        self.assertListEqual(Parser.list([('a',), ('b',), ('c',)]),
                             [F('a'), F('b'), F('c')])

        self.assertListEqual(Parser.list([[['a'], 'b'], 'c']),
                             [F('a'), F('b'), F('c')])
        self.assertListEqual(Parser.list(['a', ['b', ['c']]]),
                             [F('a'), F('b'), F('c')])

        # ---------------------------------------------------------------------
        # Unittest: eval()
        self.assertListEqual(Parser.eval(F('a')), [F('a')])
        self.assertListEqual(Parser.eval(function), [F(function)])
        self.assertListEqual(Parser.eval('function'), [F('function')])
        self.assertListEqual(Parser.eval(('function',)), [F('function')])
        self.assertListEqual(Parser.eval(['function']), [F('function')])

    def test_BaseDecorator(self):
        """Unittest: Base Decorator"""

        # ---------------------------------------------------------------------
        # Unittest: BaseDecorator
        self.assertTrue(hasattr(BaseDecorator, "__init__"))
        self.assertTrue(hasattr(BaseDecorator, "__post_init__"))
        self.assertTrue(hasattr(BaseDecorator, "__call__"))
        self.assertTrue(hasattr(BaseDecorator, "decorator"))

        # BaseDecorator is an abstract class
        try:
            BaseDecorator()
        except TypeError:
            pass
        else:
            raise AssertionError

        # ---------------------------------------------------------------------
        # Unittest: Decorator class inherited from BaseDecorator
        class Decorator(BaseDecorator):
            pass

        self.assertTrue(hasattr(Decorator, "__init__"))
        self.assertTrue(hasattr(Decorator, "__post_init__"))
        self.assertTrue(hasattr(Decorator, "__call__"))
        self.assertTrue(hasattr(Decorator, "decorator"))

        # Decorator has not overwritten the decorator() method
        try:
            Decorator()
        except TypeError:
            pass
        else:
            raise AssertionError

        # Override the decorator() method
        class Decorator(BaseDecorator):
            def decorator(self, *args: object, **kwargs: object) -> object:
                return True

        # This is not really a reasonable call to Decorator, but ok...
        d = Decorator()
        self.assertIsInstance(d, BaseDecorator)
        self.assertIsInstance(d, Decorator)
        self.assertIsNone(d._substitute)
        self.assertTupleEqual(d._args, ())
        self.assertDictEqual(d._kwargs, {})
        self.assertTupleEqual(d._deco_args, ())
        self.assertDictEqual(d._deco_kwargs, {})
        self.assertEqual(d._call_method, d.__post_init__)
        self.assertTrue(d.decorator())

        # Invalid call to Decorator with deco params (1. deco is not None!)
        try:
            Decorator()()
        except AttributeError:
            pass
        else:
            raise AssertionError

        # Valid call to Decorator without any parameters
        prnt = Decorator(print)
        self.assertEqual(prnt._substitute, print)
        self.assertTupleEqual(prnt._args, ())
        self.assertDictEqual(prnt._kwargs, {})
        self.assertTupleEqual(prnt._deco_args, ())
        self.assertDictEqual(prnt._deco_kwargs, {})
        self.assertEqual(prnt._call_method, prnt.decorator)
        self.assertTrue(prnt.decorator())

        # Valid call to Decorator without deco params
        prnt = Decorator(print, 1, key="value")
        self.assertEqual(prnt._substitute, print)
        self.assertTupleEqual(prnt._args, (1,))
        self.assertDictEqual(prnt._kwargs, dict(key="value"))
        self.assertTupleEqual(prnt._deco_args, ())
        self.assertDictEqual(prnt._deco_kwargs, {})
        self.assertEqual(prnt._call_method, prnt.decorator)
        self.assertTrue(prnt.decorator())

        # Valid call to Decorator with empty deco params
        prnt = Decorator()(print, 1, key="value")
        self.assertEqual(prnt._substitute, print)
        self.assertTupleEqual(prnt._args, (1,))
        self.assertDictEqual(prnt._kwargs, dict(key="value"))
        self.assertTupleEqual(prnt._deco_args, ())
        self.assertDictEqual(prnt._deco_kwargs, {})
        self.assertEqual(prnt._call_method, prnt.decorator)
        self.assertTrue(prnt.decorator())

        # Valid call to Decorator with keyword deco params
        prnt = Decorator(b="any stuff")(print, 1, key="value")
        self.assertEqual(prnt._substitute, print)
        self.assertTupleEqual(prnt._args, (1,))
        self.assertDictEqual(prnt._kwargs, dict(key="value"))
        self.assertTupleEqual(prnt._deco_args, ())
        self.assertDictEqual(prnt._deco_kwargs, dict(b="any stuff"))
        self.assertEqual(prnt._call_method, prnt.decorator)
        self.assertTrue(prnt.decorator())

        # Valid call to Decorator with deco params (1. deco is None!)
        prnt = Decorator(None, 2, b="any stuff")(print, 1, key="value")
        self.assertEqual(prnt._substitute, print)
        self.assertTupleEqual(prnt._args, (1,))
        self.assertDictEqual(prnt._kwargs, dict(key="value"))
        self.assertTupleEqual(prnt._deco_args, (2,))
        self.assertDictEqual(prnt._deco_kwargs, dict(b="any stuff"))
        self.assertEqual(prnt._call_method, prnt.decorator)
        self.assertTrue(prnt.decorator())

        # Invalid call to Decorator with deco params (1. deco is not None!)
        prnt = Decorator(2, 3, b="any stuff")(print, 1, key="value")
        try:
            self.assertEqual(prnt._substitute, 2)
        except AttributeError:
            pass
        else:
            raise AssertionError


# -----------------------------------------------------------------------------
# Execution
if __name__ == "__main__":
    unittest.main()
