#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This very simple class module holds general information
            about your app; which can be imported across the project
            for various uses.

:Platform:  Windows | Python 3.6+
:Developer: J Berendt
:Email:     support@s3dev.uk

:Comments:  This module is designed to be reused by other apps with
            very little modification. Ideally, you should only need to
            update the private :class:`~_About` class constants.

:Example:
    Example code use::

        from <myapp>.about import appinfo

        appinfo.description
        > 'What this app is all about.'

"""

import os
import sys
from ppk._version import __version__


class _About:
    """A private class which holds app infomation."""

    _APP_NAME = 'ppk'
    _AUTHOR = 'J Berendt'
    _AUTHOR_EMAIL = 'jeremy.berendt@rolls-royce.com'
    _COMPANY = 'Rolls-Royce, plc.'
    _COPYYEAR = '2023'
    _COPYRIGHT = f'Copyright {_COPYYEAR} | {_COMPANY}'
    _DESC = 'Python library and dependency integrity checking utility.'
    _GUI = False
    _ICON_NAME = 'icon.ico'
    _ICON_SUBDIR = 'config'
    _IS_EXE = False
    _LICENSE = 'GPL-3'
    _PLATFORM = 'Python 3.6+'
    _SCRIPT_NAME = 'ppk/ppk.py'
    _SECURITY = 'UNCLASSIFIED'
    _SHORT_DESC = 'PyPI package checker'
    _SHORT_NAME = 'ppk'
    _TITLE = 'ppk'
    _URL = ''
    _VERSION = __version__
    _EXE_NAME = f'{_SHORT_NAME}.exe'

    def __init__(self):
        """Class initialiser."""
        self._module_path = self._get_module_path()

    @property
    def app_name(self) -> str:
        """The app's proper name.

        This name is displayed in the MSI loader, and like interfaces.

        """
        return self._APP_NAME

    @property
    def author(self) -> str:
        """The app's author(s).

        This field is used primarily by the setup file.

        """
        return self._AUTHOR

    @property
    def author_email(self) -> str:
        """The app's author(s)' email address(es).

        This field is used primarily by the setup file.

        """
        return self._AUTHOR_EMAIL

    @property
    def base(self):
        """Define the executable base as used by cx_Freeze.

        This property is used for the ``base`` parameter in the
        ``executables`` parameter of cx_Freeze's ``setup()`` method.

        """
        return self._set_base()

    @property
    def company(self):
        """The development company."""
        return self._COMPANY

    @property
    def copyright(self):
        """The app's copyright statement."""
        return self._COPYRIGHT

    @property
    def copyyear(self):
        """The app's copyright statement year."""
        return self._COPYYEAR

    @property
    def description(self):
        """A brief description about this app."""
        return self._DESC

    # @property
    # def executables(self) -> list:
    #     """A list containing ``cx_Freeze``'s ``Executable`` class
    #     and it's defined parameters.

    #     This list is passed directly into the ``executables`` parameter
    #     of the :func:`~cx_Freeze.setup` function.

    #     """
    #     return self._set_executables() if self._IS_EXE else None

    @property
    def icon_path(self) -> str:
        """Path to the app icon, if available."""
        return self._get_icon_path()

    @property
    def license(self) -> str:
        """Type of license used by the app."""
        return self._LICENSE

    @property
    def package_path(self) -> str:
        """Full path to the package base.

        This method relies on the package directory being this module's
        directory.

        """
        return self._module_path

    @property
    def platform(self) -> str:
        """The app's Python platform (version)."""
        return self._PLATFORM

    @property
    def security(self) -> str:
        """The app's security classification."""
        return self._SECURITY

    @property
    def short_description(self) -> str:
        """A short desc of the app; used in the Win properties window."""
        return self._SHORT_DESC

    @property
    def short_name(self) -> str:
        """The app's short name, or alias. This will be the name of the EXE."""
        return self._SHORT_NAME

    @property
    def title(self) -> str:
        """A short title for the app."""
        return self._TITLE

    @property
    def url(self) -> str:
        """URL to the downloadable package."""
        return self._URL

    @property
    def version(self) -> str:
        """The version number."""
        return self._VERSION

    def _get_icon_path(self) -> str:
        """Set the path to the app icon.

        Returns:
            If the icon file exists (e.g. ``./icons/icon.ico``), the full
            path is returned.  If the file does not exist, ``None`` is
            returned.

        """
        path = os.path.join(self._module_path, self._ICON_SUBDIR, self._ICON_NAME)
        if os.path.exists(path):
            ico_path = path
        else:
            print('An icon does not exist.')
            ico_path = None
        return ico_path

    @staticmethod
    def _get_module_path():
        """Set the path to this module."""
        path = os.path.dirname(os.path.realpath(__file__))
        return path

    def _set_base(self):
        """Set the ``base`` value used for the ``executables`` property.

        Returns:
            If the ``sys.platform`` is 'win32' and this is a GUI app,
            return 'Win32GUI'.  Otherwise return ``None``.

        """
        base = 'Win32GUI' if all([sys.platform == 'win32', self._GUI is True]) else None
        return base

    # def _set_executables(self):
    #     """Build and return the ``executables`` list."""
    #     executables = None
    #     if self._IS_EXE:
    #         import cx_Freeze
    #         executables = [cx_Freeze.Executable(self._SCRIPT_NAME,
    #                                             base=self.base,
    #                                             targetName=self._EXE_NAME,
    #                                             icon=self.icon_path,
    #                                             copyright=self._COPYRIGHT)]
    #     return executables


appinfo = _About()
