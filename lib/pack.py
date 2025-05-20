#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:App:       pack.py
:Purpose:   This program is used to download Python packages from PyPI
            and verify the integrity of these packages to ensure they
            are deemed 'safe' for use in a sensitive environment.

            Essentially, this program wraps ``pip download`` and runs
            MD5 integrity and vulnerability checks for the package and
            its downloaded dependencies.

            If the package and its dependencies have passed the checks,
            they - along with the testing report/log - are added to an
            encrypted archive file and stored on the user's Desktop for
            transfer to the secured environment.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error

import hashlib
import itertools
import os
import re
import socket
import shutil
import subprocess as sp
from argparse import Namespace
from collections import defaultdict
from datetime import datetime as dt
from glob import glob
from utils4.crypto import crypto
from utils4.user_interface import ui
# locals
from lib.utilities import utilities
from lib.vtests import Tests
from lib.pip import Download


class PPKPacker:
    """Primary worker class for package integrity checks and packing.

    Args:
        args (argparse.Namespace): The Namespace object directly from
            the peoject's argument parser.

    """

    # List the tests to be run here.
    # These are method names from the libs.tests.Tests class.
    _TESTS = ['md5', 'snyk']

    def __init__(self, args: Namespace):
        """Package check class initialiser."""
        self._args = args           # All arguments parsed from the CLI
        self._abi = 'unset'         # The ABI tag, as parsed from the package filename.
        self._ofname = None         # The name of the outfile (no extension).
        self._md5 = None            # Package's MD5 digest from PyPI
        self._pass = False          # *Overall* passing flag for the entire test.
        self._passflags = []        # *Overall* passing flag from each test.
        self._pkg = None            # Name of the primary package (per CLI).
        self._pkg_dl = None         # Downloaded package name (wheel, or tar.gz)
        self._pkg_version = 'unset' # Package version, as parsed from the filename.
        self._py_version = 'unset'  # Python version for which the packages are downloaded.
        self._platform = 'unset'    # Platform for which the packages are downloaded.
        self._p_key = None          # Full path to the key file.
        self._p_log = None          # Full path to the log file.
        self._tmpdir = None         # Full path to the temp directory

    def main(self) -> int:
        """Main entry-point and process controller method.

        :Processes:

            - Normalise and set the package name.
            - Create the temporary download / working directory.
            - Run ``pip download`` via a subprocess call, using the
              arguments passed into the CLI by the user.
            - Obtain the package's version number, and ABI by parsing the
              filename of the downloaded wheel.
            - Build the name of the output files: archive, log and key.
            - Verify the wheels by performing validation / security tests.
            - Write a log file containing the results of the tests.
            - If the tests pass, bundle the package and its dependencies
              into an encrypted archive file on the user's desktop.
            - Remove the temporary download directory.
            - Print a summary report to the terminal.

        Returns:
            int: 0 if the download and checks pass successfully,
            otherwise 1.

        """
        self._set_package_name()
        self._make_download_directory()
        # Only process if the target package was downloaded.
        if self._pip_download():
            self._get_package_version_number()
            self._build_archive_name()
            self._verify_wheels()
            self._log_summary()
            self._copy_requirements_file()
            self._create_archive()
            self._cleanup()
            self._print_summary()
        return 0 if self._pass else 1

    def _build_archive_name(self):
        """Build the archive name, based on platform compatibility tags.

        Build a string following the convention, per the PyPA
        specification platform compatibility tag rules::

            pkg_name-pkg_version-python_version-abi_tag-platform_tag

        If downloading from a requirements file, the archive filename
        convention is::

            frz-username-datetime-pkg_name-pkg_version-python_version-abi-platform

        Otherwise, the archive filename convention is::

            pkg_name-pkg_version-python_version-abi-platform

        """
        if self._args.from_req:
            self._ofname = (f'frz-'
                            f'{utilities.get_username()}-'
                            f'{dt.now().strftime("%Y%m%d%H%M%S")}-'
                            f'{self._pkg}-'
                            f'{self._pkg_version}-'
                            f'{self._py_version}-'
                            f'{self._abi}-'
                            f'{self._platform}')
        else:
            self._ofname = (f'{self._pkg}-'
                            f'{self._pkg_version}-'
                            f'{self._py_version}-'
                            f'{self._abi}-'
                            f'{self._platform}')
            if self._args.python_version:
                self._ofname += f'-{self._args.python_version[0]}'

    def _cleanup(self, force: bool=False):
        """Class tear-down and internal cleanup method.

        Args:
            force (bool): Force a cleanup. This is (generally) used when
                a pip download fails, causing the ``self._pass`` to equal
                ``False``, negating the cleanup.

        :Actions:

            The following actions are performed *if* the ``--no_cleanup``
            flag is not passed as an argument *and* the checks have
            passed:

                - The temp directory is deleted, along with its contents.

        """
        if (not self._args.no_cleanup and self._pass) or force:
            for f in glob(os.path.join(self._tmpdir, '*')):
                os.unlink(f)
            os.removedirs(self._tmpdir)

    def _copy_requirements_file(self):
        """Copy the requirements file (if applicable) into the temp dir.

        Rationale:
            If a requirements file was used for downloading packages,
            this file is copied into the local temp directory and renamed
            using the outfile convention. This will be packed into the
            archive for transport to the server's pip repository.

        """
        if self._args.from_req:
            shutil.copy(src=self._pkg,
                        dst=os.path.join(self._tmpdir, f'{self._ofname}.txt'))

    def _create_archive(self):
        """Create an archive file from the contents of the temp directory.

        If the verification has passed, the new encrypted archive file
        is created on the user's Desktop. Otherwise, the archive is not
        created.

        Note:
            If the path to the archive already exists, it will be
            *deleted* and replaced.

        :Flags:

            The flags used in the 7z command are as follows:

                - ``a``: *Add* files to the archive.
                - ``-mx3``: Use compression level 3. This should be
                  faster than the default (5), with relatively the same
                  size on disk, as ``.whl`` files are already
                  compressed.
                - ``-mhe=on``: Encrypt the header data so the contents
                  of the archive cannot be viewed without entering the
                  decryption password.
                - ``-mmt=on``: Use multi-threading when creating the
                  archive.

        .. versionchanged: 0.2.0.dev1
           Updated to create an encrypted, password protected, archive
           file.

        """
        if self._pass:
            print('\nCreating archive ... ', end='')
            files = glob(os.path.join(self._tmpdir, '*'))
            fname, hash_ = self._generate_archive_filename()
            opath = os.path.join(utilities.get_desktop(), fname)
            cmd = ['7z', 'a', '-mx3', '-mhe=on', '-mmt=on', f'-p{hash_}', opath]
            cmd_ = cmd + files
            if os.path.exists(opath):  # If the archive already exists, delete it.
                os.unlink(opath)
            with sp.Popen(cmd_, stdout=sp.PIPE, stderr=sp.PIPE) as proc:
                stdout, stderr = proc.communicate()
            if proc.returncode:
                ui.print_alert(('\nAn error occurred while creating the archive. '
                                f'Exit code: {proc.returncode}'), style='bold')
                raise RuntimeError('\n'.join(('Output from subprocess ...',
                                              stdout.decode(),
                                              stderr.decode())))
            print('Done.')

    def _generate_archive_filename(self) -> tuple[str, str]:
        """Generate the filename for the output archive.

        Returns:
            tuple[str, str]: A tuple containing the archive name and its
            hash.

        """
        fname = f'{self._ofname}.7z'
        return fname, hashlib.sha256(fname.encode()).hexdigest()

    def _get_package_version_number(self):
        """Derive the package version, by parsing the downloaded filename.

        This version is used for naming the archive and other associated
        files.

        """
        if not self._args.from_req:
            base = self._pkg_dl
            # Source packages (.tar.gz)
            if os.path.splitext(base)[1] == '.gz':
                m = re.match(r'(.*?)(?:\.tar)?\.gz', base)
                *_, self._pkg_version = m.group(1).split('-')
            # Wheels
            else:
                base_ = os.path.splitext(base)[0]
                (_,
                 self._pkg_version,
                 self._py_version,
                 self._abi,
                 self._platform,
                 *_) = base_.split('-')

    def _log(self, results: dict[list]):
        """Create a log file for this package's verification.

        Args:
            results (dict[list]): A dictionary of lists containing the
                verification results to be written to the log file.
                Each dictionary is expected to be a list of boolean
                results; one for each test carried out.

                For example::

                    {'tzdata-2023.3-py2.py3-none-any.whl': [True, True]}

        """
        header = 'datetime,host,user,package,md5,vuln,dv_c,dv_h,dv_m,dv_l,result\n'
        # Set the filenames for the *.key and *.log files.
        self._p_key = os.path.join(self._tmpdir, f'{self._ofname}__verification.key')
        self._p_log = os.path.join(self._tmpdir, f'{self._ofname}__verification.log')
        dtme = dt.now().strftime('%Y-%m-%d %H:%M')
        host = socket.gethostname()
        user = utilities.get_username()
        with open(self._p_log, 'w', encoding='utf-8') as f:
            f.write(header)
            for k, v in results.items():
                # Flatten the test results tuples.
                v_ = list(itertools.chain(*v))
                # The first two elements are the verification flags' the
                # following elements are supporting data.
                _pass = 'pass' if all(v_[:2]) else 'fail'
                self._passflags.extend(v_[:2])
                line = f'{dtme},{host},{user},{k},{",".join(map(str, v_))},{_pass}\n'
                f.write(line)

    def _log_summary(self):
        """Write the final summary lines to the log.

        Once the final result is written to the log file, a SHA256 hash
        is calculated on the log file and written to the *.key file.

        """
        with open(self._p_log, 'a', encoding='utf-8') as f:
            flag = 'PASS' if self._pass else 'FAIL'
            f.write(f'\nResult: {flag}\n')
        # Calculate the hash on the log file and write it to the key file.
        hash_ = crypto.checksum_sha256(path=self._p_log)
        with open(self._p_key, 'w', encoding='utf-8') as f:
            f.write(hash_)

    def _make_download_directory(self):
        """Create the temporary download directory."""
        self._tmpdir = os.path.join(os.path.realpath('/tmp'), os.urandom(8).hex())
        os.makedirs(self._tmpdir)

    def _set_package_name(self):
        """Normalise and set the package name.

        If the package name was provided with version constraints, these
        are removed and any hyphens are converted to underscores.

        """
        chars = ('<', '>', '=')  # Version control chars to be removed.
        self._pkg = self._args.package[0].replace('-', '_')
        # Clean: Remove the requested version from the package name.
        if set(chars).intersection(self._pkg):
            self._pkg = re.split(f'[{"".join(chars)}]', self._pkg, maxsplit=1)[0]

    def _pip_download(self) -> str | None:
        """Download the package via pip.

        Returns:
            str | None: The filename of the downloaded target package,
            otherwise None.

        """
        pipdl = Download(args=self._args, name=self._pkg, tmpdir=self._tmpdir)
        self._pkg_dl = pipdl.get()
        return self._pkg_dl is not None

    def _print_summary(self):
        """Print an end-of-processing summary to the terminal."""
        flag = 'PASSED' if self._pass else 'FAILED'
        print('\nProcessing complete.',
              f'The {self._pkg} package has: {flag}\n',
              sep='\n')
        if self._pass:
            print('There is an *encrypted* .7z archive file on your desktop which contains ',
                  'the verified packages along with the integrity check log file. This .7z ',
                  'file can be transferred to the destination and unpacked, using ppk.',
                  '',
                  sep='\n')
        else:
            print('Please check the log file for the failing packages, in:',
                  f'-- {self._tmpdir}',
                  '',
                  sep='\n')

    def _verify_wheels(self):
        """Verify the hashes for all wheel files downloaded."""
        # pylint: disable=unnecessary-dunder-call
        results = defaultdict(list)
        args = {}
        pkgs = glob(os.path.join(self._tmpdir, '*'))
        for fpath in pkgs:
            fname = os.path.basename(fpath)
            fn, ext = os.path.splitext(fname)
            # Parse .tar.gz and .zip files differently from wheels.
            if ext == '.gz':
                *pkg_, vers_ = fname[:fname.rfind('.tar.gz')].split('-')
                pkg_ = '-'.join(pkg_)
            elif ext == '.zip':
                pkg_, vers_ = fn.split('-')
            else:
                pkg_, vers_, *_ = fname.split('-')
            args = {'fpath': fpath, 'name': pkg_, 'version': vers_}
            # ----------------------------------------------------------
            #
            #        The testing loop - perform all listed tests.
            #
            # ----------------------------------------------------------
            for test in self._TESTS:
                # Run test and update results for logging.
                results[fname].append(Tests().__getattribute__(test)(**args))
        # Force failure for testing -- DEV ONLY.
        # results['six-1.16.0-py2.py3-none-any.whl'][0] = False,
        # results['six-1.16.0-py2.py3-none-any.whl'][1] = False,4,3,2,1
        # --|
        self._log(results=results)
        # Calculate the *overall* pass/fail and store to attrib for summary.
        self._pass = all(self._passflags)
