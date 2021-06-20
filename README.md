# Natas Solutions

Python 3 solution scripts for [Natas](https://overthewire.org/wargames/natas/) levels.

## SPOILER WARNING

The numbered scripts contain working solutions to the corresponding levels in the
[Natas](https://overthewire.org/wargames/natas/) "wargame". Other files may be helpful,
but won't give away solutions.

## Hints

Each solution script has a brief level description in a doc comment. Python's `help`
function will print these for you if you need a hint. For example, to print generated
documentation for natas2, you could run the command:
```
python -c "help('.02')"
```

For some levels, this will also reveal documentation for any helper functions in the
solution script. If you have already solved the level, the password will be printed, too.

_Note: At the moment, this requires a well-formed `levels.json` file. Copy `_levels_init.json`_
_to `levels.json` file if needed._

## Using the utilities

The `natas_utils` module provides some utility functions I find helpful on various levels.
My solution scripts usually import all of its contents with `from natas_utils import *`.

Utility functions for loading and storing level data depend on a `levels.json` file in the
working directory. To use those functions starting from Natas0, rename or copy `_levels_init.json`
to `levels.json`.

`recon.py` is my utility for fetching and printing pages for the various levels from the
command line. It takes a level number and optional relative path as command line arguments.