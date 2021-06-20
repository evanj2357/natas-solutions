# Natas Solutions

Python 3 solution scripts for [Natas](https://overthewire.org/wargames/natas/) levels.

## SPOILER WARNING

This repository contains solutions to the [Natas](https://overthewire.org/wargames/natas/)
"wargame". Specifically, all numbered scripts are working solutions to the corresponding
Natas levels. Other files in the public repository may be helpful, but won't give away
solutions.

## Using the utilities

The `natas_utils` module provides some utility functions I find helpful on various levels.
My solution scripts usually import all of its contents with `from natas_utils import *`.

Utility functions for loading and storing level data depend on a `levels.json` file in the
working directory. To use those functions starting from Natas0, rename or copy `_levels_init.json`
to `levels.json`.