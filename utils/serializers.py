import csv
import io
from typing import List
from itertools import chain

def unify_dicts_structures(dicts: List[dict]) -> List[dict]:
    keys = set(chain.from_iterable(dicts))
    for dict in dicts:
        dict.update({key: None for key in keys if key not in dict})
    return dicts

def to_csv_bytes(dicts: List[dict]) -> bytes:
    output_buffer = io.StringIO()
    dicts = unify_dicts_structures(dicts)
    header = dicts[0].keys()

    dicts_writer = csv.DictWriter(output_buffer, header)
    dicts_writer.writeheader()
    dicts_writer.writerows(dicts)

    return str.encode(output_buffer.getvalue())