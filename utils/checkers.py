import os
import re
from typing import List

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

def sanitize_string(string: str) -> str:
    if emoji.emoji_count(string) > 0:
        return emoji.replace_emoji(string, replace='')
    return string

def parse_measure(string: str) -> List[str]:
    measure = string.split(':')
    if len(measure) == 2:
        return measure
    else: raise ValueError()

def is_int(string: str) -> bool:
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True