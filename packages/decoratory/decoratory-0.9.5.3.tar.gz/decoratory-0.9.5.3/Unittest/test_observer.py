#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Test Observer**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Test Observer"
__module__ = "test_observer.py"
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

from decoratory.observer import (BaseObservable, BaseObserver,
                                 Observable, Observer)
from decoratory.basic import Activation, F, X


# -----------------------------------------------------------------------------
# Test functions
def cmp(iter1, iter2):
    """Compare *all* elements of F with a tuple"""
    if len(iter1) != len(iter2):
        return False
    else:
        iter1 = list(iter1)
        iter2 = list(iter2)
        iter1.sort()
        iter2.sort()
        for left, right in zip(iter1, iter2):
            if left.callee != right.callee or \
                    left.callee_args != right.callee_args or \
                    left.callee_kwargs != right.callee_kwargs:
                return False
        return True


# -----------------------------------------------------------------------------
# Test Class
# noinspection PyPep8Naming
# noinspection PyUnresolvedReferences
# noinspection PyArgumentEqualDefault
# noinspection PyPropertyAccess
class TestObserver(unittest.TestCase):

    def setUp(self):
        """Preparation"""
        pass

    def tearDown(self):
        """Wrap-up"""
        pass

    def test_nodecoration_noparams_without_brackets(self):
        """Unittest: Functions - no decoration, no parameters, no brackets"""

        # Result list
        res = list()

        # Observable
        def dog(act: str = "Brrr!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act}'")

        # Observer
        def person(say: str = "Hello?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say}'")

        # ---------------------------------------------------------------------
        # Test setup: Observable, only
        dog_obsl = Observable(dog)

        # Checks for dog_obsl
        self.assertTrue(isinstance(dog_obsl, Observable))
        self.assertIs(dog_obsl.BaseClass, BaseObservable)
        self.assertTrue(isinstance(dog_obsl.observable, dog_obsl.BaseClass))
        self.assertTrue(hasattr(dog_obsl.observable, 'register'))
        self.assertTrue(hasattr(dog_obsl.observable, 'unregister'))
        self.assertTrue(hasattr(dog_obsl.observable, 'dispatch'))
        self.assertTrue(hasattr(dog_obsl.observable, 'observers'))
        self.assertTupleEqual(dog_obsl.observable.args, ())
        self.assertDictEqual(dog_obsl.observable.kwargs, {})
        self.assertIs(dog_obsl.activate, Activation.AFTER)
        self.assertListEqual(dog_obsl.methods, [])
        self.assertIs(dog_obsl.substitute.callee, dog)
        self.assertTupleEqual(dog_obsl.substitute.callee_args, ())
        self.assertDictEqual(dog_obsl.substitute.callee_kwargs, {})
        self.assertIs(dog_obsl.__annotations__, dog.__annotations__)
        self.assertIs(dog_obsl.__doc__, dog.__doc__)
        self.assertIs(dog_obsl.__name__, dog.__name__)

        # Calls
        res.clear()
        person()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

        # ---------------------------------------------------------------------
        # Test setup: Observable & Observer
        prs_obsr = Observer(person)

        # Checks for prs_obsr
        self.assertTrue(isinstance(prs_obsr, Observer))
        self.assertIs(prs_obsr.BaseClass, BaseObserver)
        self.assertTrue(isinstance(prs_obsr.observer, prs_obsr.BaseClass))
        self.assertTupleEqual(prs_obsr.observer.args, ())
        self.assertDictEqual(prs_obsr.observer.kwargs, {})
        self.assertListEqual(prs_obsr.methods, [])
        self.assertListEqual(prs_obsr.observables, [])
        self.assertIs(prs_obsr.substitute.callee, person)
        self.assertTupleEqual(prs_obsr.substitute.callee_args, ())
        self.assertDictEqual(prs_obsr.substitute.callee_kwargs, {})
        self.assertIs(prs_obsr.__annotations__, person.__annotations__)
        self.assertIs(prs_obsr.__doc__, person.__doc__)
        self.assertIs(prs_obsr.__name__, person.__name__)

        # ---------------------------------------------------------------------
        # Calls
        res.clear()
        prs_obsr()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

    def test_nodecoration_noparams_with_empty_brackets(self):
        """Unittest: Functions - no decoration, no parameters, empty brackets"""

        # Result list
        res = list()

        # Observable
        def dog(act: str = "Brrr!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act}'")

        # Observer
        def person(say: str = "Hello?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say}'")

        # ---------------------------------------------------------------------
        # Test setup: Observable, only
        dog_obsl = Observable()(dog)

        # Checks for dog_obsl
        self.assertTrue(isinstance(dog_obsl, Observable))
        self.assertIs(dog_obsl.BaseClass, BaseObservable)
        self.assertTrue(isinstance(dog_obsl.observable, dog_obsl.BaseClass))
        self.assertTrue(hasattr(dog_obsl.observable, 'register'))
        self.assertTrue(hasattr(dog_obsl.observable, 'unregister'))
        self.assertTrue(hasattr(dog_obsl.observable, 'dispatch'))
        self.assertTrue(hasattr(dog_obsl.observable, 'observers'))
        self.assertTupleEqual(dog_obsl.observable.args, ())
        self.assertDictEqual(dog_obsl.observable.kwargs, {})
        self.assertIs(dog_obsl.activate, Activation.AFTER)
        self.assertListEqual(dog_obsl.methods, [])
        self.assertIs(dog_obsl.substitute.callee, dog)
        self.assertTupleEqual(dog_obsl.substitute.callee_args, ())
        self.assertDictEqual(dog_obsl.substitute.callee_kwargs, {})
        self.assertIs(dog_obsl.__annotations__, dog.__annotations__)
        self.assertIs(dog_obsl.__doc__, dog.__doc__)
        self.assertIs(dog_obsl.__name__, dog.__name__)

        # Calls
        res.clear()
        person()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

        # ---------------------------------------------------------------------
        # Test setup: Observable & Observer
        prs_obsr = Observer()(person)

        # Checks for prs_obsr
        self.assertTrue(isinstance(prs_obsr, Observer))
        self.assertIs(prs_obsr.BaseClass, BaseObserver)
        self.assertTrue(isinstance(prs_obsr.observer, prs_obsr.BaseClass))
        self.assertTupleEqual(prs_obsr.observer.args, ())
        self.assertDictEqual(prs_obsr.observer.kwargs, {})
        self.assertListEqual(prs_obsr.methods, [])
        self.assertListEqual(prs_obsr.observables, [])
        self.assertIs(prs_obsr.substitute.callee, person)
        self.assertTupleEqual(prs_obsr.substitute.callee_args, ())
        self.assertDictEqual(prs_obsr.substitute.callee_kwargs, {})
        self.assertIs(prs_obsr.__annotations__, person.__annotations__)
        self.assertIs(prs_obsr.__doc__, person.__doc__)
        self.assertIs(prs_obsr.__name__, person.__name__)

        # ---------------------------------------------------------------------
        # Calls
        res.clear()
        prs_obsr()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

    def test_nodecoration_params(self):
        """Unittest: Functions - no decoration, parameters"""

        # Result list
        res = list()

        # Observable
        def dog(act1: str = "Brrr", act2: str = "!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act1}{act2}'")

        # Observer
        def person(say1: str = "Hello", say2: str = "?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say1}{say2}'")

        # ---------------------------------------------------------------------
        # Test setup: Observable, only
        dog_obsl = Observable(dog, 'Woof, ', act2='Woof!')

        # Checks for dog_obsl
        self.assertTrue(isinstance(dog_obsl, Observable))
        self.assertIs(dog_obsl.BaseClass, BaseObservable)
        self.assertTrue(isinstance(dog_obsl.observable, dog_obsl.BaseClass))
        self.assertTrue(hasattr(dog_obsl.observable, 'register'))
        self.assertTrue(hasattr(dog_obsl.observable, 'unregister'))
        self.assertTrue(hasattr(dog_obsl.observable, 'dispatch'))
        self.assertTrue(hasattr(dog_obsl.observable, 'observers'))
        self.assertTupleEqual(dog_obsl.observable.args, ())
        self.assertDictEqual(dog_obsl.observable.kwargs, {})
        self.assertIs(dog_obsl.activate, Activation.AFTER)
        self.assertListEqual(dog_obsl.methods, [])
        self.assertIs(dog_obsl.substitute.callee, dog)
        self.assertTupleEqual(dog_obsl.substitute.callee_args, ('Woof, ',))
        self.assertDictEqual(dog_obsl.substitute.callee_kwargs,
                             {'act2': 'Woof!'})
        self.assertIs(dog_obsl.__annotations__, dog.__annotations__)
        self.assertIs(dog_obsl.__doc__, dog.__doc__)
        self.assertIs(dog_obsl.__name__, dog.__name__)

        # ---------------------------------------------------------------------
        # Calls
        res.clear()
        person()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Woof, Woof!'"])

        # ---------------------------------------------------------------------
        # Test setup: Observable & Observer
        prs_obsr = Observer(person, 'Ooops', say2='!')

        # Checks for prs_obsr
        self.assertTrue(isinstance(prs_obsr, Observer))
        self.assertIs(prs_obsr.BaseClass, BaseObserver)
        self.assertTrue(isinstance(prs_obsr.observer, prs_obsr.BaseClass))
        self.assertTupleEqual(prs_obsr.observer.args, ())
        self.assertDictEqual(prs_obsr.observer.kwargs, {})
        self.assertListEqual(prs_obsr.methods, [])
        self.assertListEqual(prs_obsr.observables, [])
        self.assertIs(prs_obsr.substitute.callee, person)
        self.assertTupleEqual(prs_obsr.substitute.callee_args, ('Ooops',))
        self.assertDictEqual(prs_obsr.substitute.callee_kwargs, {'say2': '!'})
        self.assertIs(prs_obsr.__annotations__, person.__annotations__)
        self.assertIs(prs_obsr.__doc__, person.__doc__)
        self.assertIs(prs_obsr.__name__, person.__name__)

        # ---------------------------------------------------------------------
        # Calls
        res.clear()
        prs_obsr()
        self.assertListEqual(res, ["person says 'Ooops!'"])
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Woof, Woof!'"])

    def test_decoration_noparams(self):
        """Unittest: Functions - decoration, no parameters"""

        # Result list
        res = list()

        # Observable
        def dog(act: str = "Brrr!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act}'")

        # Observer
        def person(say: str = "Hello?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say}'")

        # ---------------------------------------------------------------------
        # Test setup: Observable, only
        dog_obsl = Observable(None, 'deco_arg', kw='deco_kwarg')(dog)

        # Checks for dog_obsl
        self.assertTrue(isinstance(dog_obsl, Observable))
        self.assertIs(dog_obsl.BaseClass, BaseObservable)
        self.assertTrue(isinstance(dog_obsl.observable, dog_obsl.BaseClass))
        self.assertTrue(hasattr(dog_obsl.observable, 'register'))
        self.assertTrue(hasattr(dog_obsl.observable, 'unregister'))
        self.assertTrue(hasattr(dog_obsl.observable, 'dispatch'))
        self.assertTrue(hasattr(dog_obsl.observable, 'observers'))
        self.assertTupleEqual(dog_obsl.observable.args, ('deco_arg',))
        self.assertDictEqual(dog_obsl.observable.kwargs, {'kw': 'deco_kwarg'})
        self.assertIs(dog_obsl.activate, Activation.AFTER)
        self.assertListEqual(dog_obsl.methods, [])
        self.assertIs(dog_obsl.substitute.callee, dog)
        self.assertTupleEqual(dog_obsl.substitute.callee_args, ())
        self.assertDictEqual(dog_obsl.substitute.callee_kwargs, {})
        self.assertIs(dog_obsl.__annotations__, dog.__annotations__)
        self.assertIs(dog_obsl.__doc__, dog.__doc__)
        self.assertIs(dog_obsl.__name__, dog.__name__)

        # Calls
        res.clear()
        person()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

        # ---------------------------------------------------------------------
        # Test setup: Observable & Observer
        prs_obsr = Observer(None, 'deco_arg', kw='deco_kwarg')(person)

        # Checks for prs_obsr
        self.assertTrue(isinstance(prs_obsr, Observer))
        self.assertIs(prs_obsr.BaseClass, BaseObserver)
        self.assertTrue(isinstance(prs_obsr.observer, prs_obsr.BaseClass))
        self.assertTupleEqual(prs_obsr.observer.args, ('deco_arg',))
        self.assertDictEqual(prs_obsr.observer.kwargs, {'kw': 'deco_kwarg'})
        self.assertListEqual(prs_obsr.methods, [])
        self.assertListEqual(prs_obsr.observables, [])
        self.assertIs(prs_obsr.substitute.callee, person)
        self.assertTupleEqual(prs_obsr.substitute.callee_args, ())
        self.assertDictEqual(prs_obsr.substitute.callee_kwargs, {})
        self.assertIs(prs_obsr.__annotations__, person.__annotations__)
        self.assertIs(prs_obsr.__doc__, person.__doc__)
        self.assertIs(prs_obsr.__name__, person.__name__)

        # ---------------------------------------------------------------------
        # Calls
        res.clear()
        prs_obsr()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

    def test_decoration_params(self):
        """Unittest: Functions - decoration, parameters"""

        # Result list
        res = list()

        # Observable
        def dog(act1: str = "Brrr", act2: str = "!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act1}{act2}'")

        # Observer
        def person(say1: str = "Hello", say2: str = "?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say1}{say2}'")

        # ---------------------------------------------------------------------
        # Test setup: Observable, only
        dog_obsl = Observable(None, 'deco_arg', kw='deco_kwarg')(
            dog, 'Woof, ', act2='Woof!')

        # Checks for dog_obsl
        self.assertTrue(isinstance(dog_obsl, Observable))
        self.assertIs(dog_obsl.BaseClass, BaseObservable)
        self.assertTrue(isinstance(dog_obsl.observable, dog_obsl.BaseClass))
        self.assertTrue(hasattr(dog_obsl.observable, 'register'))
        self.assertTrue(hasattr(dog_obsl.observable, 'unregister'))
        self.assertTrue(hasattr(dog_obsl.observable, 'dispatch'))
        self.assertTrue(hasattr(dog_obsl.observable, 'observers'))
        self.assertTupleEqual(dog_obsl.observable.args, ('deco_arg',))
        self.assertDictEqual(dog_obsl.observable.kwargs, {'kw': 'deco_kwarg'})
        self.assertIs(dog_obsl.activate, Activation.AFTER)
        self.assertListEqual(dog_obsl.methods, [])
        self.assertIs(dog_obsl.substitute.callee, dog)
        self.assertTupleEqual(dog_obsl.substitute.callee_args, ('Woof, ',))
        self.assertDictEqual(dog_obsl.substitute.callee_kwargs,
                             {'act2': 'Woof!'})
        self.assertIs(dog_obsl.__annotations__, dog.__annotations__)
        self.assertIs(dog_obsl.__doc__, dog.__doc__)
        self.assertIs(dog_obsl.__name__, dog.__name__)

        # ---------------------------------------------------------------------
        # Calls
        res.clear()
        person()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Woof, Woof!'"])

        # ---------------------------------------------------------------------
        # Test setup: Observable & Observer
        prs_obsr = Observer(None, 'deco_arg', kw='deco_kwarg')(
            person, 'Ooops', say2='!')

        # Checks for prs_obsr
        self.assertTrue(isinstance(prs_obsr, Observer))
        self.assertIs(prs_obsr.BaseClass, BaseObserver)
        self.assertTrue(isinstance(prs_obsr.observer, prs_obsr.BaseClass))
        self.assertTupleEqual(prs_obsr.observer.args, ('deco_arg',))
        self.assertDictEqual(prs_obsr.observer.kwargs, {'kw': 'deco_kwarg'})
        self.assertListEqual(prs_obsr.methods, [])
        self.assertListEqual(prs_obsr.observables, [])
        self.assertIs(prs_obsr.substitute.callee, person)
        self.assertTupleEqual(prs_obsr.substitute.callee_args, ('Ooops',))
        self.assertDictEqual(prs_obsr.substitute.callee_kwargs, {'say2': '!'})
        self.assertIs(prs_obsr.__annotations__, person.__annotations__)
        self.assertIs(prs_obsr.__doc__, person.__doc__)
        self.assertIs(prs_obsr.__name__, person.__name__)

        # ---------------------------------------------------------------------
        # Calls
        res.clear()
        prs_obsr()
        self.assertListEqual(res, ["person says 'Ooops!'"])
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Woof, Woof!'"])

    def test_observable_activation(self):
        """Unittest: Functions - Activation"""

        # Result list
        res = list()

        # Observable
        def dog(act: str = "Brrr!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act}'")

        # Observer
        def person(say: str = "Hello?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say}'")

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

        # ---------------------------------------------------------------------
        # Decoration
        dog_obsl = Observable(dog)
        prs_obsr = Observer(observables=dog_obsl)(person)

        # Person says default
        res.clear()
        prs_obsr()
        self.assertListEqual(res, ["person says 'Hello?'"])

        # ---------------------------------------------------------------------

        # Default activation is AFTER
        self.assertIs(dog_obsl.activate, Activation.AFTER)

        # Activation: NONE
        dog_obsl.activate = Activation.NONE
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

        # Activation: BEFORE
        dog_obsl.activate = Activation.BEFORE
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["person says 'Hello?'",
                                   "dog acts 'Brrr!'"])

        # Activation: AFTER
        dog_obsl.activate = Activation.AFTER
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["dog acts 'Brrr!'",
                                   "person says 'Hello?'"])

        # Activation: BEFORE & AFTER
        dog_obsl.activate = Activation.BEFORE_AND_AFTER
        res.clear()
        dog_obsl()
        self.assertListEqual(res, ["person says 'Hello?'",
                                   "dog acts 'Brrr!'",
                                   "person says 'Hello?'"])

    def test_observable_functions(self):
        """Unittest: Functions - Interface register, unregister, dispatch"""

        # Result list
        res = list()

        # Observable
        def dog(act: str = "Woof!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act}'")

        # Observer
        def person(say: str = "Hello?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say}'")

        # ---------------------------------------------------------------------
        # Test scenario
        def test(Person, Dog):
            # Person registered as an observer of dog by decorations above
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person, say="What's up?")}))

            # Repeated registration override current registration
            Dog.observable.register(Person)
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person)}))
            Dog.observable.register(Person, say="What's up?")
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person, say="What's up?")}))

            # Unregister person as an observer of dog
            Dog.observable.unregister(Person)
            self.assertDictEqual(Dog.observable.observers(classbased=True), {})
            self.assertDictEqual(Dog.observable.observers(), dict())

            # Re-register person as an observer of dog
            Dog.observable.register(Person)
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person)}))
            Dog.observable.register(Person, say="What's up?")
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person, say="What's up?")}))

            # Unregister *all* observers of dog
            Dog.observable.unregister()
            self.assertDictEqual(Dog.observable.observers(classbased=True), {})
            self.assertDictEqual(Dog.observable.observers(), dict())

            # Re-register person as an observer of dog
            Dog.observable.register(Person)
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person)}))
            Dog.observable.register(Person, say="What's up?")
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person, say="What's up?")}))

            # Person say default
            res.clear()
            Person()
            self.assertListEqual(res, ["person says 'Hello?'"])

            # Person say customized text using positional parameter
            res.clear()
            Person("Where is my dog?")
            self.assertListEqual(res, ["person says 'Where is my dog?'"])

            # Person say customized text using keyword parameter
            res.clear()
            Person(say="Where is my dog?")
            self.assertListEqual(res, ["person says 'Where is my dog?'"])

            # Dog act default triggers person say decoration default
            res.clear()
            Dog()
            self.assertListEqual(res, ["dog acts 'Woof!'",
                                       "person says 'What's up?'"])

            # Dog act customized text triggers person say decoration default
            res.clear()
            Dog("Brrr!")
            self.assertListEqual(res, ["dog acts 'Brrr!'",
                                       "person says 'What's up?'"])

            # Initiate additional customized dispatch
            res.clear()
            Dog("Brrr!")
            Dog.observable.dispatch(observer=Person, say="Quiet, please!")
            self.assertListEqual(res, ["dog acts 'Brrr!'",
                                       "person says 'What's up?'",
                                       "person says 'Quiet, please!'"])

            # Switch notification off/on
            res.clear()
            Dog.activate = Activation.NONE
            Dog("Brrr!")
            self.assertListEqual(res, ["dog acts 'Brrr!'"])

            res.clear()
            Dog.activate = Activation.BEFORE
            Dog("Brrr!")
            self.assertListEqual(res, ["person says 'What's up?'",
                                       "dog acts 'Brrr!'"])

            res.clear()
            Dog.activate = Activation.AFTER
            Dog("Brrr!")
            self.assertListEqual(res, ["dog acts 'Brrr!'",
                                       "person says 'What's up?'"])

            res.clear()
            Dog.activate = Activation.BEFORE_AND_AFTER
            Dog("Brrr!")
            self.assertListEqual(res, ["person says 'What's up?'",
                                       "dog acts 'Brrr!'",
                                       "person says 'What's up?'"])

            Dog.activate = Activation.AFTER

        # ---------------------------------------------------------------------
        # Test: Decoration via Observable
        prs_obsr = Observer(person)
        dog_obsl = Observable(observers=F(prs_obsr, say="What's up?"))(dog)
        test(prs_obsr, dog_obsl)

        # ---------------------------------------------------------------------
        # Test: Decoration via Observer
        dog_obsl = Observable(dog)
        prs_obsr = Observer(observables=X(dog_obsl, say="What's up?"))(person)
        test(prs_obsr, dog_obsl)

    def test_observable_class_init(self):
        """Unittest: Class - init()"""

        # Result list
        res = list()

        # Observable
        class Dog:
            """A Dog Type"""

            def __init__(self, name: str = "DOG"):
                self.name = name
                res.append(f"{self.name} acts 'INIT'")

            def untouched(self):
                """Untouched by decoration"""
                res.append(f"{self.name} is untouched")

        # Observer
        class Person:
            """A Person Type"""

            def __init__(self, name: str = "PERSON"):
                self.name = name
                res.append(f"{self.name} says 'INIT'")

            def untouched(self):
                """Untouched by decoration"""
                res.append(f"{self.name} is untouched")

        # ---------------------------------------------------------------------
        # Test setup: Decoration
        Prs_obsr = Observer(Person)
        Dog_obsl = Observable(observers=Prs_obsr)(Dog)

        # Person registered as an observer of dog by decorations above
        self.assertDictEqual(Dog_obsl.observable.observers(),
                             {F(Prs_obsr): F(Prs_obsr)})

        # Init a Person
        res.clear()
        p = Prs_obsr()
        self.assertListEqual(res, ["PERSON says 'INIT'"])

        # Init a Dog with Person as an observer
        res.clear()
        d = Dog_obsl()
        self.assertListEqual(res, ["DOG acts 'INIT'", "PERSON says 'INIT'"])

        # The untouchables
        res.clear()
        p.untouched()
        self.assertEqual(res, ['PERSON is untouched'])
        res.clear()
        d.untouched()
        self.assertEqual(res, ['DOG is untouched'])

    def test_observable_class_staticmethod01(self):
        """Unittest: Class - staticmethod()"""

        # Result list
        res = list()

        # Observable
        class Dog:
            """A Dog Type"""

            @staticmethod
            def static_method(act: str = 'Woof!'):
                """To be decorated"""
                res.append(f"Dog act '{act}'")

            @staticmethod
            def static_untouched():
                """Untouched by decoration"""
                res.append(f"Dog is untouched")

        # Observer
        class Person:
            """A Person Type"""

            @staticmethod
            def static_method(say: str = 'Hello?'):
                """To be decorated"""
                res.append(f"Person say '{say}'")

            @staticmethod
            def static_untouched():
                """Untouched by decoration"""
                res.append(f"Person is untouched")

        # ---------------------------------------------------------------------
        # Test: function decoration
        Person.static_method = Observer(Person.static_method)
        Dog.static_method = Observable(
            observers=F(Person.static_method, say="What's up?"))(
            Dog.static_method)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(cmp(Dog.static_method.observable.observers().values(),
                            {F(Person.static_method, say="What's up?")}))

        # Person
        res.clear()
        Person.static_method()
        self.assertListEqual(res, ["Person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        Dog.static_method()
        self.assertListEqual(res, ["Dog act 'Woof!'",
                                   "Person say 'What's up?'"])

        # The untouchables
        res.clear()
        Person.static_untouched()
        self.assertEqual(res, ['Person is untouched'])
        res.clear()
        Dog.static_untouched()
        self.assertEqual(res, ['Dog is untouched'])

    def test_observable_class_staticmethod02(self):
        """Unittest: Class -  staticmethod()"""

        # Result list
        res = list()

        # Observable
        class Dog:
            """A Dog Type"""

            @staticmethod
            def static_method(act: str = 'Woof!'):
                """To be decorated"""
                res.append(f"Dog act '{act}'")

            @staticmethod
            def static_untouched():
                """Untouched by decoration"""
                res.append(f"Dog is untouched")

        # Observer
        class Person:
            """A Person Type"""

            @staticmethod
            def static_method(say: str = 'Hello?'):
                """To be decorated"""
                res.append(f"Person say '{say}'")

            @staticmethod
            def static_untouched():
                """Untouched by decoration"""
                res.append(f"Person is untouched")

        # ---------------------------------------------------------------------
        # Test: class decoration
        Person = Observer(methods=Person.static_method)(Person)
        Dog = Observable(observers=F(Person.static_method, say="What's up?"),
                         methods=Dog.static_method)(Dog)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(cmp(Dog.static_method.observable.observers().values(),
                            {F(Person.static_method, say="What's up?")}))

        # Person
        res.clear()
        Person.static_method()
        self.assertListEqual(res, ["Person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        Dog.static_method()
        self.assertListEqual(res, ["Dog act 'Woof!'",
                                   "Person say 'What's up?'"])

        # The untouchables
        res.clear()
        Person.static_untouched()
        self.assertEqual(res, ['Person is untouched'])
        res.clear()
        Dog.static_untouched()
        self.assertEqual(res, ['Dog is untouched'])

    def test_observable_class_classmethod01(self):
        """Unittest: Class - classmethod()"""

        # Result list
        res = list()

        # Observable
        class Dog:
            """A Dog Type"""

            @classmethod
            def class_method(cls, act: str = 'Woof!'):
                """A classmethod"""
                res.append(f"{cls.__name__} act '{act}'")

        # Observer
        class Person:
            """A Person Type"""

            @classmethod
            def class_method(cls, say: str = 'Hello?'):
                """A classmethod"""
                res.append(f"{cls.__name__} say '{say}'")

        # ---------------------------------------------------------------------
        # Test: function decoration
        Person.class_method = Observer(Person.class_method)
        Dog.class_method = Observable(
            observers=F(Person.class_method, say="What's up?"))(
            Dog.class_method)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(cmp(Dog.class_method.observable.observers().values(),
                            {F(Person.class_method, say="What's up?")}))

        # Person
        res.clear()
        Person.class_method()
        self.assertListEqual(res, ["Person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        Dog.class_method()
        self.assertListEqual(res, ["Dog act 'Woof!'",
                                   "Person say 'What's up?'"])

    def test_observable_class_classmethod02(self):
        """Unittest: Class - classmethod()"""

        # Result list
        res = list()

        # Observable
        class Dog:
            """A Dog Type"""

            @classmethod
            def class_method(cls, act: str = 'Woof!'):
                """A classmethod"""
                res.append(f"{cls.__name__} act '{act}'")

        # Observer
        class Person:
            """A Person Type"""

            @classmethod
            def class_method(cls, say: str = 'Hello?'):
                """A classmethod"""
                res.append(f"{cls.__name__} say '{say}'")

        # ---------------------------------------------------------------------
        # Test: class decoration
        Person = Observer(methods=Person.class_method)(Person)
        Dog = Observable(observers=F(Person.class_method, say="What's up?"),
                         methods=Dog.class_method)(Dog)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(cmp(Dog.class_method.observable.observers().values(),
                            {F(Person.class_method, say="What's up?")}))

        # Person
        res.clear()
        Person.class_method()
        self.assertListEqual(res, ["Person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        Dog.class_method()
        self.assertListEqual(res, ["Dog act 'Woof!'",
                                   "Person say 'What's up?'"])

    def test_observable_class_objectmethod01(self):
        """Unittest: Class - object method()"""

        # Result list
        res = list()

        # Observable
        class Dog:
            """A Dog Type"""

            def object_method(self, act: str = 'Woof!'):
                """An objectmethod"""
                res.append(f"{self.__class__.__name__} act '{act}'")

        # Observer
        class Person:
            """A Person Type"""

            def object_method(self, say: str = 'Hello?'):
                """An objectmethod"""
                res.append(f"{self.__class__.__name__} say '{say}'")

        # ---------------------------------------------------------------------
        # Test: function decoration
        Per_obsr = Person()
        Dog_obsl = Dog()

        Per_obsr.object_method = Observer(Per_obsr.object_method)
        Dog_obsl.object_method = Observable(
            observers=F(Per_obsr.object_method, say="What's up?"))(
            Dog_obsl.object_method)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(
            cmp(Dog_obsl.object_method.observable.observers().values(),
                {F(Per_obsr.object_method, say="What's up?")}))

        # Person
        res.clear()
        Per_obsr.object_method()
        self.assertListEqual(res, ["Person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        Dog_obsl.object_method()
        self.assertListEqual(res, ["Dog act 'Woof!'",
                                   "Person say 'What's up?'"])

    def test_observable_class_objectmethod02(self):
        """Unittest: Class - object method()"""

        # Result list
        res = list()

        # Observable
        class Dog:
            """A Dog Type"""

            def object_method(self, act: str = 'Woof!'):
                """An objectmethod"""
                res.append(f"{self.__class__.__name__} act '{act}'")

        # Observer
        class Person:
            """A Person Type"""

            def object_method(self, say: str = 'Hello?'):
                """An objectmethod"""
                res.append(f"{self.__class__.__name__} say '{say}'")

        # ---------------------------------------------------------------------
        # Test: object decoration
        Per_obsr = Person()
        Dog_obsl = Dog()

        Per_obsr = Observer(methods=X('object_method'))(Per_obsr)
        Dog_obsl = Observable(
            observers=F(Per_obsr.object_method, say="What's up?"),
            methods=F('object_method'))(Dog_obsl)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(
            cmp(Dog_obsl.object_method.observable.observers().values(),
                {F(Per_obsr.object_method, say="What's up?")}))

        # Person
        res.clear()
        Per_obsr.object_method()
        self.assertListEqual(res, ["Person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        Dog_obsl.object_method()
        self.assertListEqual(res, ["Dog act 'Woof!'",
                                   "Person say 'What's up?'"])


# -----------------------------------------------------------------------------
# Execution
if __name__ == "__main__":
    unittest.main()
