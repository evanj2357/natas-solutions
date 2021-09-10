# Natas Solutions

_Evan Johnson_

Python 3 solution scripts for [Natas](https://overthewire.org/wargames/natas/) levels.

Python dependencies I used in my solutions are specified in `requirements.txt` and can
be installed using the command:
```
pip install -r requirements.txt
```

## SPOILER WARNING

The `solutions` directory contains working solution scripts for the levels in the
[Natas](https://overthewire.org/wargames/natas/) "wargame". Other files may be helpful,
but won't give away solutions.

## Hints

Each solution script has a brief level description in a doc comment. Python's `help`
function will print these for you if you need a hint. For example, to print generated
documentation for natas2, you could run the command:
```
python -c "help('solutions.natas02')"
```

For some levels, this will also reveal documentation for any helper functions in the
solution script. If you have already solved the level, the password will be printed, too.

_Note: At the moment, this requires a `levels.json` file with a structure identical to_
_`_levels_init.json`. Copy `_levels_init.json` to `levels.json` file if needed (or run_
_`solve.py`)._

## Using the utilities

The `natas_utils` module provides some utility functions I find helpful on various levels.
My solution scripts usually import all of its contents with `from natas_utils import *`.

Utility functions for loading and storing level data depend on a `levels.json` file in the
working directory. To use those functions starting from Natas0, rename or copy `_levels_init.json`
to `levels.json`. `solve.py` will do this automatically if `levels.json` does not exist when
it is run.

`recon.py` is my utility for fetching and printing pages for the various levels from the
command line. It takes a level number and optional relative path as command line arguments.

### solve.py

The main script takes a single integer as a command line argument and attempts to run the
solution script for that level. To re-run solution scripts for levels 1 through `N`, use the
`--deps` flag:
```
python solve.py --deps N
```

To use this utility with your own solutions, either replace the corresponding script in
`solutions` with your own or modify `solve.py` to import solutions from elsewhere.
`solve.py` expects solutions for each level to be a module or sub-module named "natas{LEVEL}"
(where LEVEL is the 2-digit level number, left-padded with a 0 if needed). It also expects that
the module has a function `solve` with the signature
```
solve(url: str, login: LevelLogin) -> Optional[str]
```
where `LevelLogin` is an alias for `Tuple[str, str]` and contains the username and password
for the level.