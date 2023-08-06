import math
from typing import Literal, List

from tablestring.type import Alignment


def cell_string_single_line(string: str, width: int, padding: int, align: Alignment, resolve_excess_length: Literal["truncate", "raise"] = "truncate", truc_value: str = "...") -> str:

    if len(string) + (padding * 2) > width:
        if resolve_excess_length == "raise":
            raise Exception(
                f"The length of string '{string}' (+ padding of ({padding})) exceeds column width ({width}).")
        if resolve_excess_length == "truncate":
            slice_outer_index = width - ((padding * 2) + len(truc_value))
            string = f"{string[0:slice_outer_index]}{truc_value}"

    return_string = ""

    white_space = width - ((padding * 2) + len(string))

    return_string += " " * padding

    if align == "left":
        return_string += string
        return_string += " " * white_space
    if align == "center":
        if white_space % 2 != 0:
            left_space = int(math.floor(white_space / 2) + 1)
            right_space = int(math.floor(white_space / 2))
        else:
            left_space = int(white_space / 2)
            right_space = int(white_space / 2)
        return_string += " " * left_space
        return_string += string
        return_string += " " * right_space
    if align == "right":
        return_string += " " * white_space
        return_string += string

    return_string += " " * padding

    return return_string


def cell_string_multi_line(string: str, width: int, padding: int) -> List[str]:
    pass

