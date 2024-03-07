#!/usr/bin/env bash
#-------------------------------------------------------------------------
# Prog:     ppk.sh
# Desc:     This simple script wraps the call to ppk.py with the Python
#           instance, via a venv, with which it should be run.
#
# Updates:
# 27-11-23  J. Berendt  Written
#-------------------------------------------------------------------------

_dir="$( dirname "$( realpath "$0" )" )"
ppk311="/mnt/core/var/venvs/ppk311/bin/python3.11"

$ppk311 "$_dir/ppk.py" "$@"

