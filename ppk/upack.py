#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:App:       upack.py
:Purpose:   This module provides a soft (callable) wrapper around the
            embedded ``libs/upack/upack`` program, which is responsible
            for unpacking the .zip file into the securted environment.

            Additionally, the :class:`~PPKUnPacker` class contains a
            callable method for refreshing the local pip repository,
            which is designed to be called by the base ``ppk.py``
            program, after the call unpack.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     jeremy.berendt@rolls-royce.com

:Comments:  n/a

"""

import os
import subprocess as sp
from utils4.user_interface import ui


class PPKUnPacker:
    """Primary worker class for testing and upacking the downloaded
    libraries.

    The class method themselves do not perform any of the tests or
    unpacking themselves, primarily for security purposes. The actual
    verification and unpacking is performed by the ``upack`` program,
    which has been embedded into ``ppk`` as a compiled program to
    discourage any library or verification tampering.

    Args:
        fpath (str): Full path to the ``.zip`` file to be tested and
            unpacked.

    """

    _DIR_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    _DIR_UPACK = os.path.join(_DIR_ROOT, 'libs/upack')

    def __init__(self, fpath: str):
        """Unpacker class initialiser."""
        self._fpath = fpath

    def refresh(self) -> int:
        """Refresh the cluster's local pip repository.

        Returns:
            int: The exit code from the pip-refresh shell script.

        """
        cmd = ['cstmgt-pip-refresh']
        excode = self._subprocess_call(cmd=cmd)
        return excode

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
