"""
Solve one or more levels with a convenient interface.
"""

import importlib
import os
import shutil
import sys
from typing import List, NoReturn, Optional, Union

# needed for natas_utils to load data
DATA_FILE = "./levels.json"
INIT_DATA_FILE = "./_levels_init.json"
if not os.path.exists(DATA_FILE):
    shutil.copyfile(INIT_DATA_FILE, DATA_FILE)

import natas_utils

def solve(level: int) -> Optional[str]:
    level_module = importlib.import_module("solutions.natas{:02}".format(level))
    level_data = natas_utils.load_level(level)

    flag = level_module.solve(*level_data)

    if flag:
        natas_utils.store_level_password(level + 1, flag)

    return flag

def get_level_arg_or_exit(args: List[str]) -> Union[int, NoReturn]:
    if len(args) < 1:
        exit("Missing argument: level number (integer).")

    if len(args) > 1:
        print("Not supported: batch solve.\nUsing first argument only.")

    try:
        level = int(args[0])
    except:
        exit("Type error: level number must be an integer.")

    if level < 0 or level > 34:
        exit("Invalid level number: levels are numbered 0-35.")

    return level

def main():
    solve_up_to = False
    args = sys.argv[1:]
    if "--deps" in args:
        args = list(filter(lambda arg: arg != "--deps", args))
        solve_up_to = True

    level = get_level_arg_or_exit(args)

    if len(natas_utils.NATAS_DATA["logins"][level]["password"]) == 0:
        if solve_up_to:
            for l in range(level):
                solve(l)
        else:
            exit("Missing level login. Please solve the previous level first.")

    flag = solve(level)
    if flag:
        print(f"Success! natas{level} solved.")
        print(f"natas{level}:{flag}")
    else:
        print(f"Failed to solve natas{level}.")

if __name__ == "__main__":
    main()