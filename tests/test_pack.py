#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``libs/pack`` module.

:Platform:  Linux/Windows | Python 3.10+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=protected-access

import inspect
import os
from argparse import Namespace  # To emulate CLI arguments.
from ppklib.libs.utilities import utilities
try:
    from .base import TestBase
    from .testlibs import msgs
except ImportError:
    from base import TestBase
    from testlibs import msgs
# locals
from ppk.libs.pack import PPKPacker


class TestPack(TestBase):
    """Testing class used to test the ``libs/pack`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='libs/pack')

    # def setUp(self):
    #     """Run this logic *before* each test case."""
    #     self.disable_terminal_output()

    # def tearDown(self):
    #     """Run this logic *after* each test case."""
    #     self.enable_terminal_output()

    def test01a__main__preqs(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the named package with mock CLI arguments.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['preqs'],
                            'platform': None,
                            'python_version': None,
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created(opack=p)

    def test01b__main__preqs__win_amd64(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the named package with mock CLI arguments.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['preqs'],
                            'platform': ['win_amd64'],
                            'python_version': None,
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created(opack=p)

    def test01c__main__preqs__win_amd64__311(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the named package with mock CLI arguments.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['preqs'],
                            'platform': ['win_amd64'],
                            'python_version': ['311'],
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created(opack=p)

    def test01d__main__preqs__win_amd64__312(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the named package with mock CLI arguments.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['preqs'],
                            'platform': ['win_amd64'],
                            'python_version': ['312'],
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created(opack=p)

    def test01e__main__preqs__exclude(self):
        """Test the ``main`` method with an excluded package.

        :Test:
            - Download the named package with mock CLI arguments,
              including the --exclude argument.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['preqs'],
                            'platform': None,
                            'python_version': None,
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': ['packaging']})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        with self.subTest('Excludes package'):
            with open(p._p_log, 'r', encoding='ascii') as f:
                text = f.read()
            self.assertTrue('packaging' not in text)
        self._test_archive_created(opack=p)

    def test01f__main__ppklib__exclude(self):
        """Test the ``main`` method with an excluded package.

        :Test:
            - Download the named package with mock CLI arguments,
              including the --exclude argument.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        exclude = ['beautifulsoup4',
                   'certifi',
                   'charset_normalizer',
                   'colorama',
                   'idna',
                   'requests',
                   'setuptools',
                   'soupsieve',
                   'typing_extensions',
                   'urllib3',
                   'utils4']
        args = Namespace(**{'package': ['ppklib'],
                            'platform': 'win_amd64',
                            'python_version': '312',
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': exclude})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        with self.subTest('Excludes package'):
            with open(p._p_log, 'r', encoding='ascii') as f:
                text = f.read()
            self.assertTrue(all(map(lambda x: x not in text, exclude)))
        self._test_archive_created(opack=p)

    def test02a__main__utils4(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the named package with mock CLI arguments.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['utils4==1.7.0'],
                            'platform': None,
                            'python_version': None,
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created(opack=p)

    def test02b__main__utils4__win_amd64(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the named package with mock CLI arguments.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['utils4==1.7.0'],
                            'platform': 'win_amd64',
                            'python_version': None,
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created(opack=p)

    def test02c__main__utils4__win_amd64__311(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the named package with mock CLI arguments.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['utils4==1.7.0'],
                            'platform': 'win_amd64',
                            'python_version': ['311'],
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created(opack=p)

    def test02d__main__utils4__win_amd64__312(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the named package with mock CLI arguments.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['utils4==1.7.0'],
                            'platform': 'win_amd64',
                            'python_version': ['312'],
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created(opack=p)

    def test02e__main__utils4__win_amd64__312__170(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the named package with mock CLI arguments.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['utils4==1.7.0'],
                            'platform': 'win_amd64',
                            'python_version': ['312'],
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created(opack=p)

    def test02f__main__utils4__win_amd64__312__170__replace(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the named package with mock CLI arguments.
            - Download (again) to replace the existing archive.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        args = Namespace(**{'package': ['utils4==1.7.0'],
                            'platform': 'win_amd64',
                            'python_version': ['312'],
                            'from_req': False,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst1 = p.main()
        tst2 = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst1)
            self.assertEqual(0, tst2)
        self._test_archive_created(opack=p)

    def test03a__main__requirements(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the packages listed in the requirements file.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        me = inspect.stack()[0].function
        path = os.path.join(self._DIR_RESC, me, 'requirements.txt')
        args = Namespace(**{'package': [path],
                            'platform': None,
                            'python_version': None,
                            'from_req': True,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created_from_requirements(opack=p)

    def test03b__main__requirements__win_amd64(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the packages listed in the requirements file.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        me = inspect.stack()[0].function
        path = os.path.join(self._DIR_RESC, me, 'requirements.txt')
        args = Namespace(**{'package': [path],
                            'platform': ['win_amd64'],
                            'python_version': None,
                            'from_req': True,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created_from_requirements(opack=p)

    def test03c__main__requirements__win_amd64__311(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the packages listed in the requirements file.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        me = inspect.stack()[0].function
        path = os.path.join(self._DIR_RESC, me, 'requirements.txt')
        args = Namespace(**{'package': [path],
                            'platform': ['win_amd64'],
                            'python_version': ['311'],
                            'from_req': True,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created_from_requirements(opack=p)

    def test03d__main__requirements__win_amd64__312(self):
        """Test the ``main`` method as a black box.

        :Test:
            - Download the packages listed in the requirements file.
            - Verify the exit code is as expected.
            - Verify the archive was created and named as expected.
            - Remove the downloaded archive and temp directory.

        """
        me = inspect.stack()[0].function
        path = os.path.join(self._DIR_RESC, me, 'requirements.txt')
        args = Namespace(**{'package': [path],
                            'platform': ['win_amd64'],
                            'python_version': ['312'],
                            'from_req': True,
                            'no_cleanup': True,
                            'exclude': None})
        p = PPKPacker(args=args)
        tst = p.main()
        with self.subTest('Exit code'):
            self.assertEqual(0, tst)
        self._test_archive_created_from_requirements(opack=p)

# %% Helper methods

    def _test_archive_created(self, opack: PPKPacker) -> None:
        """Verify the archive was created as expected.

        This method calls a series of sub-tests which verify the package
        was downloaded and archived as expected.

        Args:
            opack (PPKPacker): The ``PPKPacker`` object used to download
                the target package.

        """
        parts = self._parse_archive_name(name=opack._ofname)
        aname, _ = opack._generate_archive_filename()
        apath = os.path.join(os.path.join(utilities.get_desktop(), aname))
        with self.subTest('Target wheel exists'):
            self.assertTrue(os.path.exists(opack._pkgpath))
        with self.subTest('Archive exists'):
            self.assertTrue(apath)
        with self.subTest('Package name'):
            self.assertEqual(opack._name, parts['name'])
        with self.subTest('Package version'):
            self.assertEqual(opack._pkg_version, parts['vers'])
        with self.subTest('Python version'):
            self.assertEqual(opack._py_version, parts['pyvers'])
        with self.subTest('Platform'):
            if not os.path.splitext(opack._pkgpath)[1] == '.gz':
                if opack._args.platform:
                    self.assertEqual(opack._platform, parts['plat'])
                else:
                    # If the platform is not requested, verify the platform is either:
                    # - any
                    # - matches the system platform
                    # - the system platform is *in* the archive name, in the case of complex
                    #   Linux platform names.
                    self.assertTrue((parts['plat'] in (utilities.get_platform(), 'any'))
                                    or (utilities.get_platform() in aname))
        with self.subTest('Requested version'):
            if opack._args.python_version:
                self.assertEqual(opack._args.python_version[0], parts['reqvers'])
            else:
                self.assertEqual(utilities.get_python_version(), parts['reqvers'])
        # Cleanup archive and downloads.
        opack._cleanup(force=True)
        self._delete_archive(path=apath)

    def _test_archive_created_from_requirements(self, opack: PPKPacker) -> None:
        """Verify the archive was created from a requirements file.

        This method calls a series of sub-tests which verify the package
        was downloaded and archived as expected.

        Args:
            opack (PPKPacker): The ``PPKPacker`` object used to download
                the target package.

        """
        parts = self._parse_archive_name(name=opack._ofname)
        aname, _ = opack._generate_archive_filename()
        apath = os.path.join(os.path.join(utilities.get_desktop(), aname))
        with self.subTest('Target wheel exists'):
            self.assertTrue(os.path.exists(opack._pkgpath))
        with self.subTest('Archive exists'):
            self.assertTrue(apath)
        with self.subTest('Package name'):
            self.assertEqual('requirements.txt', os.path.basename(opack._name))
        with self.subTest('Package version'):
            self.assertEqual('0.0.0', parts['vers'])
        with self.subTest('Platform'):
            if opack._args.platform:
                self.assertEqual(opack._platform, parts['plat'])
            else:
                # If the platform is not requested, verify the platform is either:
                # - any
                # - matches the system platform
                # - the system platform is *in* the archive name, in the case of complex
                #   Linux platform names.
                self.assertTrue((parts['plat'] in (utilities.get_platform(), 'unset'))
                                or (utilities.get_platform() in aname))
        with self.subTest('Requested version'):
            if opack._args.python_version:
                self.assertEqual(opack._args.python_version[0], parts['reqvers'])
            else:
                self.assertEqual(utilities.get_python_version(), parts['reqvers'])
        # Cleanup archive and downloads.
        opack._cleanup(force=True)
        self._delete_archive(path=apath)

    @staticmethod
    def _delete_archive(path: str) -> None:
        """Delete the archive.

        Args:
            path (str): Full path to the archive to be deleted.

        """
        if os.path.exists(path):
            os.unlink(path)

    @staticmethod
    def _parse_archive_name(name: str) -> dict:
        """Parse the archive filename.

        Args:
            name (str): Filename of the archive to be parsed.
                For example: 'preqs-0.2.0-py3-none-any-312'

        Returns:
            dict: A dictionary of::

                {'name': 'preqs',
                 'vers': '0.2.0',
                 'pyvers': 'py3',
                 'abi': 'none',
                 'plat': 'any',
                 'reqvers': '312'}

        """
        keys = ('name', 'vers', 'pyvers', 'abi', 'plat', 'reqvers')
        values = name.split('-')
        d = dict(zip(keys, values))
        if 'reqvers' not in d:
            d['reqvers'] = utilities.get_python_version()
        if 'plat' not in d:
            d['plat'] = utilities.get_platform()
        return d
