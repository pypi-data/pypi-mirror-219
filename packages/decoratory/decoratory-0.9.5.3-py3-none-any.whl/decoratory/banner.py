#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Banner**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Banner"
__module__ = "banner.py"
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

__all__ = ["__banner"]

# -----------------------------------------------------------------------------
# Libraries & Modules
import unittest
import sys

from os.path import dirname
from importlib import import_module
from decoratory.__main__ import get_file_location


# -----------------------------------------------------------------------------
# Banner Display
def __banner(title, version, date, time, docs,
             author: str = __author__,
             maintainer: str = __maintainer__,
             company: str = __company__,
             email: str = __email__,
             url: str = __url__,
             copyright: str = __copyright__,
             state: str = __state__,
             license: str = __license__,
             file_license: str = "License.txt"):
    """**Banner**

    Banner is an auxiliary module for displaying package and module
    information.
    """
    module = title.lower()
    name = title.capitalize()

    arg = sys.argv[1].strip().lower() if len(sys.argv) > 1 else "message"
    if arg in "--version":
        print(f"{module}: Version {version}, "
              f"Build {date} {time}, State '{state}'")
    elif arg in "--copyright":
        print(f"{copyright}")
    elif arg in "--license" or arg in "--licence":
        print(f"\n{'-' * 79}")
        print(f"{title} ships under the license: {license}".center(79))
        print(f"{'-' * 79}")
        file_path = get_file_location(file_license)
        if file_path is not None:
            with open(file_path, "r") as fp:
                txt = fp.read()
            print("\n" + txt)
        else:
            print("*** No additional data accessible. Please look for "
                  f"file '{file_license}' ***".center(79, " "))
        # print(f"{'-' * 79}")
        # print(f"File: {file_path}".center(79, " "))
        print(f"{'-' * 79}")
    elif arg in "--documentation":
        print()
        for doc in docs:
            print(f"{' ' + doc.__name__ + ' ':-^79s}\n")
            print(doc.__doc__)  # print(help(doc))
        print(f"{'-' * 79}")
    elif arg in "--information":
        print(f"\nPeople and contact information for module {module}:\n")
        print(f"Author    : {author}")
        print(f"Maintainer: {maintainer}")
        print(f"Company   : {company}")
        print(f"Email     : {email}")
        print(f"Web       : {url}")
    elif arg in "--test":
        try:
            print(f"\n{'-' * 70}")
            print(f" Running unit test for module: {module} ".center(70, '-'))
            print(f"{'-' * 70}\n")
            sys_path = dirname(get_file_location(f"test_{module}.py"))
            if sys_path and sys_path not in sys.path:
                sys.path.insert(0, sys_path)
            loader = unittest.TestLoader().loadTestsFromModule
            mdl = import_module(f"test_{module}")
            suite = loader(mdl)
            unittest.TextTestRunner(verbosity=2).run(suite)
        except (ModuleNotFoundError, ImportError, NameError, Exception):
            print(f"*** No unit test available for module "
                  f"{module} ***\n".center(70, " "))
        print(f"{'-' * 70}")
    else:
        print(f"""
-------------------------------------------------------------------------------
{title.upper(): ^79}
-------------------------------------------------------------------------------

{module} is a Python module you cannot execute directly from command line.
This module provides a {name} decorator.

{module} is provided under the {license} License included with this module. It 
comes without any warranty, but with the intention of saving work, time and 
improving code quality as well as productivity.

All kinds of bugs, questions, improvement suggestions, change requests etc. 
are welcome to be directed to the product maintainers email {email}.

The current version of the installed package is:
{module}: Version {version}, Build {date} {time}, State '{state}'

Syntax:   python -m decoratory.{module} [option]

Possible options are:

  -h, --help           show this help message
  -v, --version        show module {module} version information      
  -c, --copyright      show module {module} copyright statement
  -l, --license        show module {module} license statement (License.txt)
      --licence        an alias to --license
  -d, --documentation  display selected module code documentation
  -t, --test           run unit test for module {module}
  -i, --info           people and contact information

-------------------------------------------------------------------------------
{copyright: <69s}{date: >10s}
-------------------------------------------------------------------------------
""")


# -----------------------------------------------------------------------------
# Entry Point
if __name__ == '__main__':
    __banner(title=__title__,
             version=__version__,
             date=__date__,
             time=__time__,
             docs=(__banner,))
