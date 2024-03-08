#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   Load the keys and values from ``config.json`` as attributes
            of the :class:`Config` class.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

import os
from utils4.config import loadconfig


class Config:
    """Program configuration attribute container."""

    def __init__(self):
        """Config class initialiser."""
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')
        for k, v in loadconfig(filename=path).items():
            setattr(self, k, v)


config = Config()
