#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains generalised utility-based functions,
            used throughout the project.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=wrong-import-order

import os
import requests
import sys
import sysconfig


class Utilities:
    """General utility functions wrapper class."""

    @staticmethod
    def get_desktop() -> str:
        """Get the path to the user's Desktop. Works for Linux or Windows.

        Returns:
            str: The full path to the current user's Desktop, per the
            OS-specific environment variable.

        """
        if 'win' in sys.platform:
            return os.path.join(os.environ.get('USERPROFILE'), 'Desktop')
        return os.path.join(os.environ.get('HOME'), 'Desktop')

    @staticmethod
    def get_platform() -> str:
        """Return the platform."""
        os_, arch_ = sysconfig.get_platform().split('-')
        os_ = 'manylinux2014' if os_ == 'linux' else os_
        return f'{os_}_{arch_}'

    @staticmethod
    def get_python_version() -> str:
        """Return the no-dot major minor python version."""
        ma, mi, *_ = sys.version_info
        return f'{ma}{mi}'

    @staticmethod
    def get_username() -> str:
        """Get the username. Works for Linux or Windows.

        Returns:
            str: The current user's username, per the OS-specific
            environment variable.

        """
        if 'win' in sys.platform:
            return os.environ.get('USERNAME')
        return os.environ.get('USER')

    @staticmethod
    def query_pypi(pkg: str) -> dict:
        """Query the PyPI API and get the JSON for the specific package.

        The PyPI API is queried to obtain the data for the requested
        package. If successful, the returned data (in JSON format) is
        stored into the class' ``_json`` variable.

        A timeout of N seconds is setup on the GET request, in the event
        the remote server fails to respond.

        Args:
            pkg (str): Name of the package to be queried.

        Returns:
            dict: The results of the query in JSON format.

        """
        data = None
        url = f'https://pypi.org/pypi/{pkg}/json'
        with requests.get(url, timeout=5) as r:
            if r.status_code == 200:
                data = r.json()
            else:
                msg = (f'\nThe request for ({pkg}) failed with status code: {r.status_code}\n'
                       'Perhaps the package has a different name?')
                raise RuntimeWarning(msg)
        return data


utilities = Utilities()
