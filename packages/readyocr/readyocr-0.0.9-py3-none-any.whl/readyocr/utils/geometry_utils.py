import statistics 
from typing import List
from copy import deepcopy
from collections.abc import Iterable


def sort_by_position(entities: List) -> List:
    return sorted(entities, key=lambda e: (e.bbox.y + e.bbox.height, e.bbox.x))