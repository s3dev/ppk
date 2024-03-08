#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:App:       upack.py
:Purpose:   This module provides a soft (callable) wrapper around the
            embedded ``lib/upack.d/bin/upack`` program, which is
            responsible for verifying and unpacking the encrypted
            archive into the securted environment.

            Additionally, the :class:`~PPKUnPacker` class contains a
            callable method for refreshing the local pip repository,
            which is designed to be called by the base ``ppk.py``
            program, after the call unpack.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error

import os
import shutil
import subprocess as sp
import traceback
from utils4.user_interface import ui
# locals
from lib.config import config


class PPKUnPacker:
    """Primary worker class for testing and upacking the downloaded
    libraries.

    The class method themselves do not perform any of the tests or
    unpacking themselves, primarily for security purposes. The actual
    verification and unpacking is performed by the ``upack`` program,
    which has been embedded into ``ppk`` as a compiled program to
    discourage any library or verification tampering.

    Args:
        fpath (str): Full path to the ``.7z`` file to be tested and
            unpacked.

    """

    _DIR_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    _DIR_UPACK = os.path.join(_DIR_ROOT, 'lib/upack.d/bin')

    def __init__(self, fpath: str):
        """Unpacker class initialiser."""
        self._fpath = fpath

    def refresh(self) -> int:
        """Refresh the environment's local pip repository.

        Using the ``pip_refresh_prog`` key in the ``config.json`` file,
        if that program exists, it is called. Otherwise a warning
        message is displayed to the user.

        Returns:
            int: The exit code from the pip-refresh shell script.
            If an exception is found, 1 is returned.

        """
        prog = config.pip_refresh_prog
        if shutil.which(prog) is not None:
            try:
                cmd = [prog]
                excode = self._subprocess_call(cmd=cmd)
                return excode
            except Exception as err:
                ui.print_alert('\nAn error occurred while calling pip refresh.\n', style='bold')
                tbstr = traceback.format_exception(err)
                print(*tbstr, sep='\n')
                return 1  # Error code.
        else:
            prog_ = prog or 'None'  # Change name to 'None' if not populated.
            ui.print_warning(f'\nThe pip refresh program could not be found: {prog_}\n'
                             'The libraries have been unpacked, but the repo has *not* been '
                             'refreshed.\n')
        return 1  # Error code.

    def run(self) -> int:
        """Call the unpacker with the provided file path.

        Returns:
            int: Return the exit code from the ``upack`` program.

        """
        msg = f'\nVerifying and unpacking: {os.path.basename(self._fpath)} ...'
        cmd = [os.path.join(self._DIR_UPACK, 'upack'), self._fpath]
        excode = self._subprocess_call(cmd=cmd, msg=msg)
        return excode

    def _subprocess_call(self, cmd: list, msg: str=None, show_stdout: bool=False) -> int:
        """Perform a subprocess call for the given arguments.

        Args:
            cmd (list): A list containing the command to be issued.
            msg (str, optional): Start of processing message to be
                displayed. Defaults to None.
            show_stdout (bool, optional): Display the stdout stream.
                Defaults to False.

        Returns:
            int: Exit code from the subprocess call.

        """
        if msg:
            print(msg)
        with sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE) as proc:
            stdout, stderr = proc.communicate()
            if show_stdout:
                print(*stdout.decode().split('\n'), sep='\n')
            excode = proc.returncode
        if excode:
            ui.print_alert('\n'.join(stderr.decode().split('\n')))
        return excode
