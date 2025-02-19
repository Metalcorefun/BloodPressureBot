import os
import re
from typing import List
import time

import emoji

def is_valid_filename(filename: str) -> bool:
    if (not filename
            or not os.path.splitext(filename)[1]
            or contains_invalid_chars(filename, r'[\/:"*?<>|]')):
        return False
    return True

# < > : " / \ | ? *
def contains_invalid_chars(string, pattern) -> bool:
    if re.search(pattern, string):
        return True
    return False

def is_file_exists(filename: str) -> bool:
    return os.path.exists(filename)

def sanitize_string(string: str) -> str:
    if emoji.emoji_count(string) > 0:
        return emoji.replace_emoji(string, replace='')
    return string


def is_int(string: str) -> bool:
    try:
        _ = int(string)
    except ValueError:
        return False
    else:
        return True

def is_valid_time(value) -> bool:
    try:
        _ = time.strptime(value, '%H:%M')
    except ValueError:
        return False
    return True