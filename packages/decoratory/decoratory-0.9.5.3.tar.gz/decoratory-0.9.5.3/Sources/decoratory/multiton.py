#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Multiton**

    A multiton pattern is a design pattern that extends the singleton pattern.
    Whereas the singleton allows for exactly one instance per class, the
    multiton ensures one single (unique) instance per key.

    In this implementation, the key parameter can be anything that is possible
    as a key for a Python dict() dictionary, such as an immutable type or a
    callable eventually returning such an immutable type etc.

    In case of an invalid key, key is set None and with only one key value the
    multiton simply collapses to a singleton, therefore the decoration
    @Multiton resp. @Multiton() or even @Multiton(key=17) or
    @Multiton(key='some constant value') and so on always creates a singleton.

    Attributes
    ----------
    Multiton (class):
        Creates a multiton instance as a callable object.

    Methods
    -------
        None.

    Examples
    --------

    # -------------------------------------------------------------------------
    from decoratory.multiton import Multiton

    @Multiton(key=lambda spec, name: name)
    class Animal:
        def __init__(self, spec, name):
            self.spec = spec
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.spec}', '{self.name}')"

    # Create Instances
    a = Animal('dog', name='Teddy')
    b = Animal('cat', name='Molly')
    c = Animal('dog', name='Roxie')

    # Case 0: decoration @Multiton or @Multiton() or @Multiton(key=17) or ...
    #    ---> With no or fixed key the Multiton acts like a Singleton
    print(a)                        # Animal('dog', 'Teddy')
    print(b)                        # Animal('dog', 'Teddy')
    print(c)                        # Animal('dog', 'Teddy')

    # Case 1: decoration @Multiton(key=lambda spec, name: name)
    #    ---> key is a function evaluating the attribute name from __init__(..)
    print(a)                        # Animal('dog', 'Teddy')
    print(b)                        # Animal('cat', 'Molly')
    print(c)                        # Animal('dog', 'Roxie')

    # Case 2: decoration @Multiton(key=lambda spec, name: 'a' in name)
    #    ---> key is a function evaluating the attribute name from __init__(..)
    print(a)                        # Animal('dog', 'Teddy')
    print(b)                        # Animal('cat', 'Molly')
    print(c)                        # Animal('cat', 'Molly')

    # Case 3: decoration @Multiton(key="{0}".format)
    #    ---> Parameter spec is referenced as args[0] (positional)
    print(a)                        # Animal('dog', 'Teddy')
    print(b)                        # Animal('cat', 'Molly')
    print(c)                        # Animal('dog', 'Teddy')

    # Case 4: decoration @Multiton(key="{name}".format)
    #    ---> Parameter name is referenced as kwargs['name'] (keyword)
    print(a)                        # Animal('dog', 'Teddy')
    print(b)                        # Animal('cat', 'Molly')
    print(c)                        # Animal('dog', 'Roxie')

    # Case 5: decoration @Multiton(key=lambda spec, name: (spec, name))
    #    ---> One unique instance for all init values, i.e. no duplicates
    print(a)                        # Animal('dog', 'Teddy')
    print(b)                        # Animal('cat', 'Molly')
    print(c)                        # Animal('dog', 'Roxie')

    # Case 6: decoration @Multiton(key=F("my_key"))
    #    ---> Late binding with F(classmethod_string)
    #         One unique instance from a @staticmethod or @classmethod
    class Animal:
        ...
        @classmethod
        def my_key(cls, spec, name):
            return 'a' in name

    print(a)                        # Animal('dog', 'Teddy')
    print(b)                        # Animal('cat', 'Molly')
    print(c)                        # Animal('cat', 'Molly')

    # Case 7: with decoration @Multiton(key=lambda spec, name: name,
    #                                   resettable=True)
    Animal.reset()                  # Because of resettable=True
    print(Animal.get_instances())   # {}
    print(Animal.issealed())        # False     (=default)
    Animal('dog', name='Teddy')     # Animal('dog', 'Teddy')
    print(Animal.get_instances())   # {'Teddy': Animal('dog', 'Teddy')}
    Animal.seal()                   # Seal the multiton!
    print(Animal.issealed())        # True
    try:                            # Try to..
        Animal('cat', name='Molly') # .. add a new animal
    except  KeyError as ex:         # .. will fail
        print(f"Sorry {ex.args[1]}, {ex.args[0]}")
    print(Animal.get_instances())   # {'Teddy': Animal('dog', 'Teddy')}
    Animal.unseal()                 # Unseal the multiton!
    print(Animal.issealed())        # False
    Animal('cat', name='Molly')     # Now, Molly is added
    print(Animal.get_instances())   # {'Teddy': Animal('dog', 'Teddy'),
                                    #  'Molly': Animal('cat', 'Molly')}
"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Multiton"
__module__ = "multiton.py"
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

__all__ = ["Multiton"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from functools import update_wrapper
from typing import Union
from decoratory.basic import F


# -----------------------------------------------------------------------------
# Classes
class Multiton:
    """**Multiton**

    Multiton(substitute, *args, key, resettable, **kwargs)

    Attributes
    ----------
    substitute (callable|type):
        A type to be made a multiton

    key (F|callable|object|None):
        An object building the instance key

    resettable (bool):
        If True exposes a reset() method

    Methods
    -------
    seal(self) -> None:
        Seal the multiton

    unseal(self) -> None:
        Unseal the multiton

    issealed(self) -> bool:
        Multiton sealing state

    get_instances(self) -> dict:    (property)
        Returns the internal dictionary of instances

    set_instances(self) -> None:    (property)
        Sets the internal dictionary of instances

    reset(self) -> None:            (if resettable=True, only!)
        Resets the multiton instance dictionary
    """

    def __init__(self,
                 substitute: Union[type, callable, None] = None,
                 *args: object,
                 key: Union[F, callable, object, None] = None,
                 resettable: bool = False,
                 **kwargs: object) -> None:
        """Set up a multiton.

        Parameters:
            substitute (object): A type to be made a multiton
            key: (F|callable|object|None): An object building the instance key
            resettable (bool): If True exposes a reset() method

        Returns:
            self (object): Multiton decorator instance
        """
        self.__set__substitute(substitute)
        self.__key = key

        # Dictionary for unique key instances
        self._instances = dict()

        # Sealing state
        self.__sealed = False

        # If resettable == True exposes a reset() method
        if bool(resettable):
            def reset(s: object = self) -> None:
                """Define reset method"""
                s.set_instances(None)

            # Add the reset method
            setattr(self, 'reset', reset)

        # --- Decorator Arguments Template (1/2)
        if self.__get__substitute() is not None:
            # Decoration without parameter(s)
            self.__set__substitute(
                F(self.__get__substitute(), *args, **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

    def __call__(self, *args, **kwargs):
        """Apply the decorator"""
        # --- Decorator Arguments Template (2/2)
        if self.__get__substitute() is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())
            return self
        else:  # *** Decorator ***
            # If no current values, take defaults
            if args or kwargs:
                subst = F(self.__get__substitute().callee, *args, **kwargs)
            else:
                subst = self.__get__substitute()

            # Calculate key from callable or read key from arguments
            try:
                if isinstance(self.__key, F):  # classmethod or staticmethod
                    if callable(self.__key.callee):
                        d_key = F(self.__key.callee, *subst.callee_args,
                                  **subst.callee_kwargs).eval()
                    else:
                        d_key = F(
                            getattr(self.substitute.callee, self.__key.callee),
                            *subst.callee_args, **subst.callee_kwargs).eval()
                elif callable(self.__key):  # function
                    d_key = F(self.__key, *subst.callee_args,
                              **subst.callee_kwargs).eval()
                else:  # Value
                    d_key = self.__key
                instance = self._instances.get(d_key, None)
            except (TypeError, Exception):  # Default is None
                d_key = None
                instance = self._instances.get(d_key, None)

            # Create and store new or return existing instance (by key)
            if instance is None:
                if self.__sealed:
                    raise KeyError(f"{self.__name__} is sealed.", d_key)
                instance = self._instances.setdefault(d_key, subst.eval())

            return instance

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)

    def get_instances(self) -> dict:
        """Returns the internal dictionary of instances"""
        return self._instances

    def set_instances(self, value: dict = None) -> None:
        """Sets the internal dictionary of instances"""
        self._instances = value if isinstance(value, dict) else dict()

    instances = property(get_instances, set_instances)

    # Methods
    def seal(self) -> None:
        """Seal multiton.

        Parameters:
            None.

        Returns:
            None.
        """
        self.__sealed = True

    def unseal(self) -> None:
        """Unseal multiton .

        Parameters:
            None.

        Returns:
            None.
        """
        self.__sealed = False

    def issealed(self) -> bool:
        """Multiton sealing state

        Parameters:
            None.

        Returns:
            True/False (bool): Sealing state.
        """
        return self.__sealed


# -----------------------------------------------------------------------------
# Entry Point
if __name__ == '__main__':
    import decoratory.multiton as module
    from decoratory.banner import __banner as banner

    banner(title=__title__,
           version=__version__,
           date=__date__,
           time=__time__,
           docs=(module, Multiton),
           author=__author__,
           maintainer=__maintainer__,
           company=__company__,
           email=__email__,
           url=__url__,
           copyright=__copyright__,
           state=__state__,
           license=__license__)
