#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the functionality related to calls to
            ``pip``.

:Platform:  Linux/Windows | Python 3.10+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""

from __future__ import annotations

import os
import re
import sys
import subprocess as sp
from utils4.user_interface import ui


class Download:
    """Processing related to the ``pip download`` command.

    Args:
        args (Namespace): The ``Namespace`` object directly from the
            argument parser. This will contain all the parameters
            required for the download.
        name (str): Normalised, cleaned target package name. Used to find
            the target package in the temp downloads directory.
        tmpdir (str): Full path to the temp (download) directory.

    """

    def __init__(self, args: Namespace, name: str, tmpdir: str):  # noqa  # pylint: disable=undefined-variable
        """Download class initialiser."""
        self._args = args
        self._name = name
        self._tmpdir = tmpdir
        self._pkg = None        # Filename of the downloaded target package.

    def get(self) -> str | None:
        """Collect the specified package.

        Returns:
            str | None: The filename of the downloaded target package,
            otherwise None.

        """
        self._download()
        self._find()
        return self._pkg

    def _download(self):
        """Using a subprocess call, download the package via pip.

        By design, the output from ``pip`` is streamed to the terminal
        and therefore not captured by a ``subprocess.PIPE``.

        The ``--only-binary=:all:`` argument is added to the pip command
        if *any* of the following arguments are passed, as this is a
        requirement by pip, unless ``--no_deps`` is specified.

            - ``--only_binary``
            - ``--platform``
            - ``--python_version``

        If the ``pip download`` fails for any reason (returning a
        non-zero exit code), the program is exited with an exit code of 1
        and a force cleanup is performed.

        """
        report_and_exit = False  # Escape if the pip error thrown is not expected.
        # Use the package name as passed into the CLI, as this *might* contain
        # a specific version to be downloaded.
        cmd = ['pip', 'download', '-d', self._tmpdir]
        # Alter the pip command with user args from the CLI.
        if self._args.from_req:
            # Download from requirements file.
            cmd.extend(['-r', self._args.package[0]])
        else:
            # Download from package name.
            cmd.extend([self._args.package[0]])
        if not self._args.use_local:
            cmd.extend(['-i', 'https://pypi.org/simple/'])
        if self._args.platform:
            cmd.extend(['--platform', self._args.platform[0]])
        if self._args.python_version:
            cmd.extend(['--python-version', self._args.python_version[0]])
        # Always add the ---only-binary=:all: arg if the platform or
        # py version are specified. This is a requirement by pip, unless
        # --no-deps is specified.
        if any((self._args.only_binary, self._args.platform, self._args.python_version)):
            if self._args.no_deps:
                cmd.extend(['--no-deps'])
            else:
                cmd.extend(['--only-binary', ':all:'])
        print('')  # Add blank line before pip output to aid readability.
        # No stdout pipe is used so pip's output streams to the terminal.
        with sp.Popen(cmd, stderr=sp.PIPE) as proc:
            _, stderr = proc.communicate()
            if proc.returncode:
                print('', stderr.decode(), sep='\n')
                if b'no matching distribution' in stderr.lower():
                    # Fix the missing (library not found) issue.
                    self._fix_missing(msg=stderr)
                else:
                    report_and_exit = True
                if report_and_exit:
                    ui.print_alert('\n[ERROR]: An error was thrown from pip. Exiting.\n')
                    self._cleanup(force=True)
                    sys.exit(1)
        print('')  # Add blank line after pip output to aid readability.

    def _find(self) -> None:
        """Find the downloaded target package and store the filename.

        For case agnostic searching, (e.g. in the case of libraries such
        as 'sqlalchemy' which downloads as 'SQLAlchemy'), the search is
        carried out using a :func:`filter` applied to :func:`os.listdir`.

        If the target package is found in the download directory, the
        filename is stored to the :attr:`_pkg`: attribute.

        """
        if not self._args.from_req:
            name = self._name.translate({45: '*', 95: '*'}).lower()  # Discard - and _ chrs.
            pkg = list(filter(lambda x: x.lower().startswith(name), os.listdir(self._tmpdir)))
            if pkg:
                self._pkg = os.path.basename(pkg[0])

    def _fix_missing(self, msg: bytes):
        """Update the requirements file to fix the missing binary library.

        Args:
            msg (bytes): Error message thrown by pip to stderr, directly
                from the ``subprocess.Popen.communicate`` call.

        Using pip's error message, the offending package name is
        extracted. Then, a line (as shown below) is appended to the
        requirements file, instructing pip to download the source
        distribution::

            --no-binary=<pkg_name>

        Finally, re-call :meth:`_pip_download` to re-try the download
        with the modified requirements file.

        """
        pkg = self._parse_err__no_matching_dist(msg=msg)
        # Test if a requirements file is being used.
        if all((pkg, self._args.from_req)):
            ui.print_(f'Modifying the requirements file and trying again for {pkg} ...',
                      fore='brightcyan')
            with open(self._args.package[0], 'a', encoding='utf-8') as f:
                f.write(f'--no-binary={pkg}')
            self._download()

    @staticmethod
    def _parse_err__no_matching_dist(msg: bytes) -> str:
        """Extract the relevent package name from the error message.

        Args:
            msg (bytes): Error message directly from the
                Popen.communicate stderr pipe.

        Returns:
            str: Name of the offending package.

        """
        # pylint: disable=line-too-long
        pkg = None
        msg = msg.decode()
        rexp = re.compile(r'error: no matching distribution found for (?P<pkg>[\w-]+)(?:\\x1b)?', re.I)
        s = rexp.search(msg)
        if s:
            pkg = s.groupdict().get('pkg')
        return pkg
