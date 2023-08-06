#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Decoratory**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Decoratory"
__module__ = "__main__.py"
__author__ = "Martin Abel"
__maintainer__ = "Martin Abel"
__credits__ = ["Martin Abel"]
__company__ = "eVation"
__email__ = "python@evation.eu"
__url__ = "http://evation.eu"
__copyright__ = f"(c) copyright 2020-2023, {__author__}, {__company__}"
__created__ = "2020-01-01"
__version__ = "0.9.5.3"
__date__ = "2023-07-17"
__time__ = "15:53:35"
__state__ = "Beta"
__license__ = "MIT"

__all__ = ["get_file_location"]

# -----------------------------------------------------------------------------
# Libraries & Modules
import unittest
import sys

from os.path import dirname, join, basename
from glob import glob
from site import getsitepackages, getusersitepackages
from importlib import import_module

# -----------------------------------------------------------------------------
# Parameters
module = __title__.lower()
name = __title__.capitalize()


# -----------------------------------------------------------------------------
# Functions
def get_file_location(filename: str = "License.txt"):
    """Finds an installed data file in any OS dependent installation"""
    # Look in all possible site package locations, global and user
    if isinstance(getsitepackages(), list):
        package_locations = getsitepackages()
    else:
        package_locations = [getsitepackages()]
    if isinstance(getusersitepackages(), list):
        package_locations.extend(getusersitepackages())
    else:
        package_locations.append(getusersitepackages())
    # Try to find the RECORD file in dist/version folder in package_location
    target_path = None
    for package_location in package_locations:
        try:
            # Read RECORD file
            record = join(package_location,
                          f"{__title__.lower()}-{__version__}.dist-info",
                          "RECORD")
            with open(record, "r") as f_rec:
                rec_lines = f_rec.readlines()
            # Search in lines for the given filename
            for rec_line in rec_lines:
                file_path, sep, *skip = rec_line.partition(",")
                if file_path and str(file_path).endswith(filename):
                    try:
                        path = join(package_location, file_path)
                        with open(path, "r") as fp:
                            fp.read(1)  # something to read...?
                        target_path = path
                        break
                    except (FileNotFoundError, Exception):
                        continue
        except (FileNotFoundError, Exception):
            continue
    return target_path


# -----------------------------------------------------------------------------
# A Module Entry Point
def main():
    """Package information"""
    arg = sys.argv[1].strip().lower() if len(sys.argv) > 1 else "message"
    if arg in "--version":
        print(f"{module}: Version {__version__}, "
              f"Build {__date__} {__time__}, State '{__state__}'")
    elif arg in "--copyright":
        print(f"{__copyright__}")
    elif arg in "--license" or arg in "--licence":
        print(f"\n{'-' * 79}")
        print(f"{__title__} ships under the license: {__license__}".center(79))
        print(f"{'-' * 79}")
        file_path = get_file_location("License.txt")
        if file_path is not None:
            with open(file_path, "r") as fp:
                txt = fp.read()
            print("\n" + txt)
        else:
            print("*** No additional data accessible. Please look for "
                  "file 'License.txt' ***".center(79, " "))
        # print(f"{'-' * 79}")
        # print(f"File: {file_path}".center(79, " "))
        print(f"{'-' * 79}")
    elif arg in "--test":
        try:
            print(f"\n{'-' * 70}")
            print(f" Running unit tests for all modules ".center(70, '-'))
            print(f"{'-' * 70}\n")
            loader = unittest.TestLoader().loadTestsFromModule
            sys_path = dirname(get_file_location(f"test_basic.py"))
            if sys_path and sys_path not in sys.path:
                sys.path.insert(0, sys_path)
            for mdl in glob(join(sys_path, "test_*.py")):
                mdl = basename(mdl)[:-3].lower()
                print(f"\n{' ' + mdl + ' ' :-^70s}\n")
                mdl = import_module(mdl)
                suite = loader(mdl)
                unittest.TextTestRunner(verbosity=2).run(suite)
        except (ModuleNotFoundError, ImportError, NameError, Exception):
            print(f"*** No unit test available for package "
                  f"{module} ***\n".center(70, " "))
        print(f"{'-' * 70}")
    elif arg in "--information":
        print(f"\nPeople and contact information for package {module}:\n")
        print(f"Author    : {__author__}")
        print(f"Maintainer: {__maintainer__}")
        print(f"Company   : {__company__}")
        print(f"Email     : {__email__}")
        print(f"Web       : {__url__}")
    else:
        print(f"""
-------------------------------------------------------------------------------
{__title__.upper(): ^79}
-------------------------------------------------------------------------------

{module} is a Python package you cannot execute directly from command line.

The package provides a framework for Python decorators as well as concrete 
implementations of useful decorators, e.g. Singleton, Multiton, Observable 
and a configurable Wrapper.

{module} is provided under the {__license__} License included with this \
module. It 
comes without any warranty, but with the intention of saving work, time and 
improving code quality as well as productivity.

All kinds of bugs, questions, improvement suggestions, change requests etc. 
are welcome to be directed to the product maintainers email {__email__}.

The current version of the installed package is:
{module}: Version {__version__}, Build {__date__} {__time__}, \
State '{__state__}'

Syntax:   python -m {module}[.module] [option]

For information about the whole package the module command can be left empty, 
for special module information one of the following modules can be addressed:

{'singleton, multiton, wrapper, observer': ^79s}

Possible options are:

  -h, --help           show this help message
  -v, --version        show {module}[.module] version information      
  -c, --copyright      show {module}[.module] copyright statement
  -l, --license        show {module}[.module] license statement (License.txt)
      --licence        an alias to --license
  -t, --test           run unit tests for {module}[.module]
  -i, --info           people and contact information

Example: Display license statement for the multiton module:

{'python -m decoratory.multiton --license': ^79s}
         
-------------------------------------------------------------------------------
{__copyright__: <69s}{__date__: >10s}
-------------------------------------------------------------------------------
""")


# -----------------------------------------------------------------------------
# Execution
if __name__ == '__main__':
    main()
