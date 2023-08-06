#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Wrapper**

    A wrapper encloses the original function with an

     - (optional) before call functionality, and/or
     - (optional) after  call functionality, and/or

    substitutes the original functionality with an

     - (optional) replace call functionality.

    All three decorator parameters, before, after and replace, can be combined
    with each other and support both single callables and (nested) lists of
    F-types (imported from module decoratory.basic, see below for details).
    In addition, replace supports passing results from successive replacement
    calls through an optional keyword argument named result (default value is
    None).

    Attributes
    ----------
    Wrapper (class):
        Creates a wrapper instance as a callable object.

    Methods
    -------
        None.

    Examples
    --------

    # -------------------------------------------------------------------------
    from decoratory.wrapper import Wrapper

    # Case 1: Dynamic decoration with decorator arguments, only
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    # Function call with default parameters
    some_function()                 # value = 'original'
    some_function = Wrapper(some_function, value="changed")
    some_function()                 # value = 'changed'

    # -------------------------------------------------------------------------
    from decoratory.wrapper import Wrapper
    from decoratory.basic import F

    # Case 2: Decoration with before and after functionalities
    def print_message(message: str = "ENTER"):
        print(message)

    @Wrapper(before=print_message, after=F(print_message, "LEAVE"))
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    some_function()                 # ENTER
                                    # value = 'original'
                                    # LEAVE

    # Case 3: Decoration with replace functionality
    def replace_wrapper(value: str="replace"):
        # 1. Edit the call parameters for the original functionality
        value = value.upper()
        # 2. Execute original functionality with modified call parameters
        result = some_function.substitute.callee(value)             # (1)
        # 3. Edit the result and return this modified result
        return f"result: '{result}'"

    @Wrapper(replace=replace_wrapper)
    def some_function(value: str = "original"):
        print(f"value = '{value}'")
        return value

    result = some_function()        # value = 'REPLACE'
    print(result)                   # result: 'REPLACE'

    # Case 4: Decoration with before, after and multiple replacements
    def print_message(message: str = "UNDEFINED"):
        print(message)

    def replacement_printer(add: int = 1, *, result=None):
        result += add if isinstance(result, int) else 0
        print(f"result = {result}")
        return result

    @Wrapper(before=F(print, "ENTER"), # Python's print()
             replace=[F(replacement_printer, 1, result=0),
                      F(replacement_printer, 3),
                      F(replacement_printer, 5)],
             after=F(print_message, "LEAVE"))
    def result_printer(message: str = "UNKNOWN"):
        print(message)

    result_printer()                # ENTER         (before)
                                    # result = 1    (replacement_printer, 1)
                                    # result = 4    (replacement_printer, 3)
                                    # result = 9    (replacement_printer, 5)
                                    # LEAVE         (after)
                                    # 9             (output default_printer)

    @Wrapper(before=F(print, "BEFORE init"), after=F(print, "AFTER init"))
    class Animal:
        def __init__(self, name):
            self.name = name
            print("RUNNING init")

    # Case 5: Decoration of a class always refers to __init__
    a = Animal(name='Teddy')        # BEFORE init
                                    # RUNNING init
                                    # AFTER init

    # Case 6: Define a private wrapper library
    before_wrapper = Wrapper(before=F(print, "BEFORE"))
    after_wrapper = Wrapper(after=F(print, "AFTER"))

    # Multiple decorations for specialized functionality encapsulation
    @before_wrapper
    @after_wrapper
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    some_function()                 # BEFORE
                                    # value = 'original'
                                    # AFTER
"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Wrapper"
__module__ = "wrapper.py"
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

__all__ = ["Wrapper"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from functools import update_wrapper
from typing import Union
from decoratory.basic import F, Parser


# -----------------------------------------------------------------------------
# Classes
class Wrapper:
    """**Wrapper**

    Wrapper(substitute, *args, before, replace, after, **kwargs)

    Attributes
    ----------
    substitute (callable|type):
        A type to be made a wrapper

    before (callable|list):
        (List of) callable(s) to be executed before substitute

    replace (callable|list):
        (List of) callable(s) replacing the substitute

    after (callable|list):
        (List of) callable(s) to be executed after substitute

    Methods
    -------
        None.
    """

    def __init__(self,
                 substitute: Union[type, callable, None] = None,
                 *args: object,
                 before: Union[callable, list, None] = None,
                 replace: Union[callable, list, None] = None,
                 after: Union[callable, list, None] = None,
                 **kwargs: object) -> None:
        """Set up a wrapper.

        Parameters:
            substitute (object): A type to be made a wrapper.
            before (object): (List of) callable(s) to be executed before
            replace (object): (List of) callable(s) replacing the substitute
            after (object): (List of) callable(s) to be executed after

        Returns:
            self (object): Wrapper decorator instance
        """
        self.__set__substitute(substitute)
        self.__set__before(before)
        self.__set__replace(replace)
        self.__set__after(after)

        # --- Decorator Arguments Template (1/2)
        if self.__get__substitute() is not None:
            # Decoration without parameter(s)
            self.__set__substitute(
                F(self.__get__substitute(), *args, **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

    def __call__(self, *args, **kwargs):
        # --- Decorator Arguments Template (2/2)
        if self.__get__substitute() is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())
            return self
        else:  # *** Decorator ***
            # Action BEFORE
            if self.__get__before():
                for before in self.__get__before():
                    before.eval()

            # Delegation vs. REPLACE
            result = None
            if self.__get__replace():
                # Replacement
                if args or kwargs:
                    for replace in self.__get__replace():
                        d = replace.callee.__kwdefaults__
                        if d and 'result' in d:
                            d['result'] = result
                        result = F(replace.callee, *args, **kwargs).eval()
                else:
                    for replace in self.__get__replace():
                        d = replace.callee.__kwdefaults__
                        if d and 'result' in d:
                            d['result'] = result
                        result = replace.eval()
            else:
                # Delegation
                if args or kwargs:
                    result = F(self.__get__substitute().callee, *args,
                               **kwargs).eval()
                else:
                    result = self.__get__substitute().eval()

            # Action AFTER
            if self.__get__after():
                for after in self.__get__after():
                    after.eval()

            return result

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)

    def __get__before(self):
        return self.__before

    def __set__before(self, value):
        self.__before: list = Parser.eval(value)

    before = property(__get__before)

    def __get__replace(self):
        return self.__replace

    def __set__replace(self, value):
        self.__replace: list = Parser.eval(value)

    replace = property(__get__replace)

    def __get__after(self):
        return self.__after

    def __set__after(self, value):
        self.__after: list = Parser.eval(value)

    after = property(__get__after)


# -----------------------------------------------------------------------------
# Simple example
if __name__ == '__main__':
    import decoratory.wrapper as module
    from decoratory.banner import __banner as banner

    banner(title=__title__,
           version=__version__,
           date=__date__,
           time=__time__,
           docs=(module, Wrapper),
           author=__author__,
           maintainer=__maintainer__,
           company=__company__,
           email=__email__,
           url=__url__,
           copyright=__copyright__,
           state=__state__,
           license=__license__)
