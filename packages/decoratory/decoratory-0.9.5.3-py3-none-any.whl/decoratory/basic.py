#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Basic**

    Basic provides a framework for define, parse, interpret and evaluate
    decorator arguments. It generates and resolves (nested) lists of tuples of
    decorator argument objects between their native forms and F/X structure
    representations.

    Attributes
    ----------
    Activation: IntFlag
        Relative time flags for activity control.

    F: Type
        A wrapper for callee(*callee_args, **callee_kwargs) semantics.

    X: Type(F)
        A cross-wrapper for callee vs. *callee_args and/or **callee_kwargs.

    Parser: Type
        Parser to resolve the function/class decoration argument language.

    Methods
    -------
    None.
"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Basic"
__module__ = "basic.py"
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

__all__ = ["Activation", "Parser", "F", "X", "BaseDecorator"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from abc import ABC, abstractmethod
from enum import IntFlag
from typing import Union
from functools import update_wrapper


# -----------------------------------------------------------------------------
# Classes
class Activation(IntFlag):
    # noinspection GrazieInspection
    """Relative time flags for activity control.

        NONE                    No activation
        BEFORE                  Activation before action
        AFTER                   Activation after action
        BEFORE_AND_AFTER        Activation before and after action
        """
    NONE = 0x00
    BEFORE = 0x01
    AFTER = 0x02
    BEFORE_AND_AFTER = BEFORE | AFTER


class F:
    """A wrapper for callee(*callee_args, **callee_kwargs) semantics.

    The caller is designed as a read-only property, since it is used as a key
    to collect F objects in sets.

    The eval() method applies the callee property to its callee_args and/or
    callee_kwargs:
      - If callee is a callable, it is applied directly to the arguments,
      - If callee is a string, eval() is applied to the same-named method of
        the object passed to eval().

    Attributes
    ----------
        callee: callable or str     (getter property)
        callee_args: object
        callee_kwargs: object

    Methods
    -------
    eval(self, obj=None)
        Evaluate the value of callee(callee_args, callee_kwargs)

    Example
    -------

    from decoratory.basic import F

    # Define a callable
    def sandwich(anything="", toast: str = "|"):
        return f"{toast}{anything}{toast}"

    # Case 1: Function argument is a callable
    f = F(sandwich)                 # F(sandwich), sandwich(): ||
    print(f"{repr(f)}, {str(f)}: {f.eval()}")
    f = F(sandwich, 3)              # F(sandwich, 3), sandwich(3): |3|
    print(f"{repr(f)}, {str(f)}: {f.eval()}")
    f = F(sandwich, 'A')            # F(sandwich, "A"), sandwich("A"): |A|
    print(f"{repr(f)}, {str(f)}: {f.eval()}")
    f = F(sandwich, 3, '*')         # F(sandwich, 3, "*"), sandwich(3, "*"):
    print(f"{repr(f)}, {str(f)}: {f.eval()}")   # *3*
    f = F(sandwich, 3, toast='*')   # F(sandwich, 3, toast="*"), sandwich(
    print(f"{repr(f)}, {str(f)}: {f.eval()}")   # 3, toast="*"): *3*

    # Define a method
    class A:
        def sandwich(self, anything="", toast: str = "|"):
            return f"{toast}{anything}{toast}"

    # Case 2: Function argument is a method name
    f = F("sandwich")               # F("sandwich"), sandwich(): ||
    print(f"{repr(f)}, {str(f)}: {f.eval(obj=A())}")
    f = F("sandwich", 3)            # F("sandwich", 3), sandwich(3): |3|
    print(f"{repr(f)}, {str(f)}: {f.eval(obj=A())}")
    f = F("sandwich", 'A')          # F("sandwich", "A"), sandwich("A"): |A|
    print(f"{repr(f)}, {str(f)}: {f.eval(obj=A())}")
    f = F("sandwich", 3, '*')       # F("sandwich", 3, "*"), sandwich(3, "*"):
    print(f"{repr(f)}, {str(f)}: {f.eval(obj=A())}")    # *3*
    f = F("sandwich", 3, toast='*') # F("sandwich", 3, toast="*"), sandwich(
    print(f"{repr(f)}, {str(f)}: {f.eval(obj=A())}")    # 3, toast="*"): *3*
    """
    __slots__ = ('__callee', 'callee_args', 'callee_kwargs')

    @staticmethod
    def __quote(qs: str = "", qq: str = '"') -> str:
        """Special str quotes"""
        return f"{qq}{qs}{qq}" if isinstance(qs, str) else str(qs)

    def __init__(self, callee, *callee_args, **callee_kwargs):
        self.__set__callee(callee)
        self.callee_args = callee_args
        self.callee_kwargs = callee_kwargs

    def __repr__(self):
        s = str(self.__class__.__name__) + '('
        if callable(self.__callee):
            s += str(self.__callee.__name__)
        else:
            s += self.__class__.__quote(self.__callee)
        if self.callee_args:
            s += ', ' + ', '.join(self.__class__.__quote(k)
                                  for k in self.callee_args)
        if self.callee_kwargs:
            s += ', ' + ', '.join((str(k) + '=' + self.__class__.__quote(v))
                                  for k, v in self.callee_kwargs.items())
        return s + ')'

    def __str__(self):
        if callable(self.__callee):
            s = str(self.__callee.__name__) + '('
        else:
            s = str(self.__callee) + '('
        if self.callee_args:
            s += ', '.join(self.__class__.__quote(k)
                           for k in self.callee_args)
        if self.callee_kwargs:
            if self.callee_args:
                s += ', '
            s += ', '.join((str(k) + '=' + self.__class__.__quote(v))
                           for k, v in self.callee_kwargs.items())
        return s + ')'

    def __hash__(self):
        return hash(self.__callee)  # Read only object key, see init above

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__callee == other.__callee
        elif callable(other) or isinstance(other, str):
            return self.__callee == other
        else:
            return False

    def __iter__(self):
        return iter([self.__callee, self.callee_args, self.callee_kwargs])

    def __next__(self):
        pass  # __iter__ delegates to list iterator

    def eval(self, obj=None):
        """Evaluate the value of callee(callee_args, callee_kwargs)"""
        if callable(self.__callee):
            # Assume default function semantics
            return self.__callee(*self.callee_args, **self.callee_kwargs)
        elif isinstance(self.__callee, str):
            # Assume an instance method semantics
            if obj is None:
                # Assume obj is in first positional argument args[0]
                if self.callee_args:
                    obj = self.callee_args[0]
                    if hasattr(obj, self.__callee):
                        return getattr(obj, self.__callee)(
                            *self.callee_args[1:], **self.callee_kwargs)
            elif hasattr(obj, self.__callee):
                # Assume this obj as the instance of __callee
                return getattr(obj, self.__callee)(
                    *self.callee_args, **self.callee_kwargs)

        # In all other cases
        raise TypeError(f"'{self.__callee}' cannot be evaluated.")

    # Getter, Setter, Properties
    def __get__callee(self):
        return self.__callee

    def __set__callee(self, value: Union[callable, str]):
        self.__callee = value  # Read-only object key, see init above

    callee = property(__get__callee)


class X(F):
    """A cross-wrapper for callee vs. *callee_args and/or **callee_kwargs.

    Technically, X is equivalent to F. Both share the same code, the same
    syntax, but they follow different semantics:
       - F is a wrapper for a callee and its OWN arguments, whereas
       - X is a wrapper for a callee and arguments for another caller

    Although X can be substituted by F, it is recommended to use X to indicate
    that the callee and the specified arguments do not belong to each other,
    for reasons of code clarity.
    """
    pass


class Parser:
    """Parser to resolve the function/class decoration argument language.

    A Parser to resolve the function/class decoration argument language where
    a callable is mandatory and the optional arguments have empty defaults
    into a list of F-structures.

    Syntax:
        Parser.eval(item) -> [F(callable|method_name, *args, **kwarg), ...]

    Production:
        item        :=  list | tuple | F | callable | str | None
        list        := [list | tuple | F | callable | str | None]
            [..,list,..]                -> [..,*list,..]
        tuple       := (..,) | (..,..) | (..,..,..)
            (callable|str,)             -> F(callable|str)
            (callable|str, (..))        -> F(callable|str, *(..))
            (callable|str, {..})        -> F(callable|str, **{..})
            (callable|str, (..), {..})  -> F(callable|str, *(..), **{..})
        F           := F(..) | F(..,..) | F(..,..,..)
            F(callable|str)             -> F(callable|str)
            F(callable|str, *a)         -> F(callable|str, *a)
            F(callable|str, **kwa)      -> F(callable|str, **kwa)
            F(callable|str, *a, **kwa)  -> F(callable|str, *a, **kwa)
        callable    := callable
            callable                    -> F(callable)
        str         := str
            str                         -> F(str)
        None        := None
            None                        -> []
    """

    @classmethod
    def eval(cls, item: Union[list, tuple, F, callable, str, None]) -> list:
        """Format data, resolve and collect as F-structures in a flat list

        list        -> cls.list         (see below)
        tuple       -> [cls.tuple]      (see below)
        F(..,..,..) -> [F(.,.,.)]
        callable    -> [F(callable)]
        string      -> [F(string)]
        None        -> []               (empty list)
        """
        result = list()
        if item is None:
            pass  # Capture the no list default into an empty list
        elif isinstance(item, F):
            result.append(item)
        elif callable(item) or isinstance(item, str):
            result.append(F(item))
        elif isinstance(item, tuple):
            result.append(cls.tuple(item))
        elif isinstance(item, list):
            result.extend(cls.list(item))
        else:
            raise TypeError(f"Object '{item}' cannot be parsed.")
        return result

    @classmethod
    def list(cls, list_obj: list) -> list:
        """Resolve (nested) list recursively.

        Loop over list (iterable) and resolve list items:

        list        -> [..., cls.list]       (extend recursively)
        tuple       -> [..., cls.tuple]      (see below)
        F(..,..,..) -> [..., F(..,..,..)]
        callable    -> [..., F(callable)]
        str         -> [..., F(str)]
        None        -> [...]
        """
        result = list()
        for li in list_obj:
            if isinstance(li, list):
                result.extend(cls.list(li))
            elif isinstance(li, tuple):
                result.append(cls.tuple(li))
            elif isinstance(li, F):
                result.append(li)
            elif callable(li) or isinstance(li, str):
                result.append(F(li))
            elif li is None:
                pass
            else:
                raise TypeError(f"List element '{li}' cannot be parsed.")
        return result

    @classmethod
    def tuple(cls, tuple_obj: tuple) -> F:
        """Resolve tuple and create an F

        Analyse a tuple and map it into an F structure:

        (callable|str,)             -> F(callable|str)
        (callable|str, (..))        -> F(callable|str, *(..))
        (callable|str, {..})        -> F(callable|str, **{..})
        (callable|str, (..), {..})  -> F(callable|str, *(..), **{..})
        """
        if len(tuple_obj) == 1 and \
                (callable(tuple_obj[0]) or isinstance(tuple_obj[0], str)):
            return F(tuple_obj[0])
        elif len(tuple_obj) == 2 and \
                (callable(tuple_obj[0]) or isinstance(tuple_obj[0], str)):
            if isinstance(tuple_obj[1], tuple):
                return F(tuple_obj[0], *tuple_obj[1])
            elif isinstance(tuple_obj[1], dict):
                return F(tuple_obj[0], **tuple_obj[1])
        elif len(tuple_obj) == 3 and \
                (callable(tuple_obj[0]) or isinstance(tuple_obj[0], str)) and \
                isinstance(tuple_obj[1], tuple) and \
                isinstance(tuple_obj[2], dict):
            return F(tuple_obj[0], *tuple_obj[1], **tuple_obj[2])

        # No match
        raise TypeError(f"Tuple '{tuple_obj}' cannot be parsed.")


class BaseDecorator(ABC):
    """A base decorator class from which wrapper type decorators are inherited.

    BaseDecorator is an (abstract) class that implements a special case of the
    *Decorator Arguments Methods Template* for wrapper decorators, for which
    primarily only the abstract method decorator() needs to be overridden.

    Attributes
    ----------
        None.

    Methods
    -------
    decorator(self, *args: object, **kwargs: object) -> object
        Abstract method that must be overwritten with the wrapper code.

    Example
    -------

    from decoratory.basic import BaseDecorator
    from typing import Union

    # A simple example wrapper inherited from BaseDecorator
    class SomeWrapper(BaseDecorator):
        def __init__(self,
                     substitute: Union[type, callable, None] = None,
                     *args: object,
                     message_before: str = "ENTER",
                     message_after: str = "LEAVE",
                     **kwargs: object) -> None:

            super().__init__(substitute, *args, **kwargs)

            # Collect all *additional* named parameters
            self._message_before = message_before
            self._message_after = message_after

        def decorator(self, *args: object, **kwargs: object) -> object:
            # *** Decorator Code ***

            # Action *before* original code
            print(f"{self.__name__}: {self._message_before}")

            # Delegation to original code
            if args or kwargs:
                result = self._substitute(*args, **kwargs)
            else:
                result = self._substitute(*self._args, **self._kwargs)

            # Action *after* original code
            print(f"{self.__name__}: {self._message_after}")

            return result           # Result from original code


    # Case 1: Static decoration with the inherited SomeWrapper
    @SomeWrapper(message_before="Calc started...",
                 message_after="... Calc done!")
    def add(a: int, b: int):
        print(f"Result: {a + b}")   # Print added numbers

    # Execute the decorated add function
    add(2, 3)                       # add: Calc started...
                                    # Result: 5
                                    # add: ... Calc done!

    # Case 2: Dynamic decoration with the inherited SomeWrapper
    def add(a: int, b: int):
        print(f"Result: {a + b}")   # Print added numbers

    add = SomeWrapper(add, 1, b=2)  # Tailored defaults a=1, b=2

    # Execute the decorated add function
    add()                           # add: ENTER    (deco  default)
                                    # Result: 3     (extra default)
                                    # add: LEAVE    (deco  default)
    """

    def __init__(self,
                 substitute: Union[type, callable, None] = None,
                 *args: object,
                 **kwargs: object) -> None:
        # Collect all named parameters
        self._substitute = substitute

        # --- Decorator Arguments Template (1/2)
        if self._substitute is not None:
            # Decoration without parameter(s)
            self._args = args  # Positional  params to substitute
            self._kwargs = kwargs  # Keyword params to substitute
            self._deco_args = ()  # Opt: no positional decorator params
            self._deco_kwargs = {}  # Opt: no keyword  decorator params
            update_wrapper(self, self._substitute, updated=())

            # Instantiation is done, assign the decorator
            self._call_method = self.decorator
        else:
            # Decoration with parameter(s)
            self._args = ()  # Opt: no positional params to substitute
            self._kwargs = {}  # Opt: no keyword  params to substitute
            self._deco_args = args  # Positional  decorator params
            self._deco_kwargs = kwargs  # Keyword decorator params

            # Instantiation not yet completed, assign the post init
            self._call_method = self.__post_init__

    def __post_init__(self, *args: object, **kwargs: object) -> object:
        """Post-init completion of the instantiation of the callable object"""

        # --- Decorator Arguments Template (1/2)
        if args:
            # Decoration with parameter(s)
            self._substitute: Union[type, callable, None] = args[0]  # Assign!
            self._args = args[1:]  # Positional params to substitute: args[1:]
            self._kwargs = kwargs  # Keyword    params to substitute: kwargs
            update_wrapper(self, self._substitute, updated=())

            # Instantiation is done, assign the decorator
            self._call_method = self.decorator

            return self  # Return the completed instance
        else:
            raise AttributeError("No substitute found!")

    def __call__(self, *args: object, **kwargs: object) -> object:
        return self._call_method(*args, **kwargs)  # Delegation

    @abstractmethod
    def decorator(self, *args: object, **kwargs: object) -> object:
        """Abstract method that must be overwritten with the wrapper code."""
        raise NotImplementedError(f"{self.decorator.__qualname__} missing!")


# -----------------------------------------------------------------------------
# Entry Point
if __name__ == '__main__':
    from decoratory.banner import __banner as banner
    from decoratory import basic

    banner(title=__title__,
           version=__version__,
           date=__date__,
           time=__time__,
           docs=(BaseDecorator, F, X, Parser, Activation),
           author=__author__,
           maintainer=__maintainer__,
           company=__company__,
           email=__email__,
           url=__url__,
           copyright=__copyright__,
           state=__state__,
           license=__license__)
