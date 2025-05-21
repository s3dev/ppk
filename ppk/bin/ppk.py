#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the main entry-point and controller
            method for the ``ppk`` project.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

:Example:

    Example for downloading a package (pandas) from PyPI::

        $ cd /path/to/ppk
        $ python3 ppk.py pandas


    Example for unpacking the pandas ZIP file archive, containing wheels
    packed by the packer above::

        $ cd /path/to/ppk
        $ python3 ppk.py /path/to/pandas-2.1.1-cp311-cp311-manylinux2014_x86_64.7z


    For more usage examples, please refer to the README file.

"""
# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=wrong-import-position

import os
import sys
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from utils4.user_interface import ui
# locals
from ppk.libs.argparser import argparser
from ppk.libs.pack import PPKPacker
from ppk.libs.upack import PPKUnPacker


class Main:
    """Project entry-point and primary controlling class."""

    def __init__(self):
        """Main project class initialiser."""
        self._args = None

    def run(self):
        """Program entry-point and primary public callable.

        When called, this method triggers the argument parser and
        determines the program's execution path, as directed by the
        parsed arguments.

        Addditionally, this method contains the primary exception handler
        for the project. All exceptions triggered by the underlying
        modules and methods are expected to 'bubble-up' into this method
        for reporting to the user.

        """
        try:
            self._parse_args()
            if self._args.unpack:
                unpack = PPKUnPacker(fpath=self._args.package[0])
                excode = unpack.run()
                if not excode:
                    # Refresh only if the unpack succeeds.
                    excode = unpack.refresh()
            else:
                excode = PPKPacker(args=self._args).main()
            if not excode:
                print('Done.\n')
        except Exception as err:
            ui.print_alert('\nThe following error occured, halting execution:\n', style='bold')
            tbstr = traceback.format_exception(err)
            print(*tbstr, sep='\n')
            excode = 73
        sys.exit(excode)

    def _parse_args(self):
        """Parse the command line arguments."""
        argparser.parse()
        self._args = argparser.args


if __name__ == '__main__':
    m = Main()
    m.run()
