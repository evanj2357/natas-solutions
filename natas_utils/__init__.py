from .natas_utils import (
    PW_FORMAT,
    LevelLogin,
    LevelData,
    extract_candidate_passwords,
    flag_file_abspath,
    load_level,
    store_level_password,
    try_level_login
)

NATAS_DATA = dict.copy(natas_utils.NATAS_DATA)