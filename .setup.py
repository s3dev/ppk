#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:App:       setup.py
:Purpose:   Python library packager.

:Version:   0.2.1
:Platform:  Linux/Windows | Python 3.5
:Developer: J Berendt
:Email:     support@s3dev.uk

:Example:
    Create source and wheel distributions::

        $ cd /path/to/package
        $ python setup.py sdist bdist_wheel

    Simple installation::

        $ cd /path/to/package/dist
        $ pip install <pkgname>-<...>.whl

    git installation::

        $ pip install git+file:///<drive>/path/to/package

    github installation::

        $ pip install git+https://github.com/s3dev/<pkgname>

"""

import os
from setuptools import setup, find_packages
# locals
from lib.about import appinfo as ai


class Setup:
    """Create a dist package for this library."""

    PACKAGE         = ai.app_name
    VERSION         = ai.version
    PLATFORMS       = ai.platform
    DESC            = ai.description
    AUTHOR          = ai.author
    AUTHOR_EMAIL    = ai.author_email
    URL             = ai.app_name
    LICENSE         = ai.license
    MIN_PYTHON      = '>=3.6'
    ROOT            = os.path.realpath(os.path.dirname(__file__))
    PACKAGE_ROOT    = os.path.join(ROOT, PACKAGE)
    INCL_PKG_DATA   = True
    CLASSIFIERS     = ['Programming Language :: Python :: 3',
                       'Programming Language :: Python :: 3.6',
                       'Programming Language :: Python :: 3.7',
                       'Programming Language :: Python :: 3.8',
                       'Programming Language :: Python :: 3.9',
                       'Programming Language :: Python :: 3.10',
                       'Programming Language :: Python :: 3.11',
                       'Programming Language :: Python :: 3.12',
                       'Development Status :: 4 - Beta',
                       'Environment :: Console',
                       'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                       'Operating System :: Microsoft :: Windows',
                       'Operating System :: POSIX :: Linux',
                       'Topic :: Utilities']

    # PACKAGE REQUIREMENTS
    REQUIRES        = ['beautifulsoup4', 'requests', 'utils4']
    PACKAGES        = find_packages()

    # ADD DATA AND DOCUMENTATION FILES
    DATA_FILES      = []
    PACKAGE_DATA    = {}

    def run(self):
        """Run the setup."""
        setup(name=self.PACKAGE,
              version=self.VERSION,
              platforms=self.PLATFORMS,
              python_requires=self.MIN_PYTHON,
              description=self.DESC,
              author=self.AUTHOR,
              author_email=self.AUTHOR_EMAIL,
              maintainer=self.AUTHOR,
              maintainer_email=self.AUTHOR_EMAIL,
              url=self.URL,
              license=self.LICENSE,
              packages=self.PACKAGES,
              install_requires=self.REQUIRES,
              data_files=self.DATA_FILES,
              include_package_data=self.INCL_PKG_DATA,
              classifiers=self.CLASSIFIERS,
              package_data=self.PACKAGE_DATA)

if __name__ == '__main__':
    Setup().run()
