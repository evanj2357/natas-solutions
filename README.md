# Natas Solutions

Python 3 solution scripts for [Natas](https://overthewire.org/wargames/natas/) levels.

## SPOILER WARNING

The numbered scripts contain working solutions to the corresponding levels in the
[Natas](https://overthewire.org/wargames/natas/) "wargame". Other files may be helpful,
but won't give away solutions.

## Using the utilities

The `natas_utils` module provides some utility functions I find helpful on various levels.
My solution scripts usually import all of its contents with `from natas_utils import *`.

Utility functions for loading and storing level data depend on a `levels.json` file in the
working directory. To use those functions starting from Natas0, rename or copy `_levels_init.json`
to `levels.json`.

`recon.py` is my utility for fetching and printing pages for the various levels from the
command line. It takes a level number and optional relative path as command line arguments.