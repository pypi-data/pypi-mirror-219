import math
from typing import List, Optional

from textframe.typing import Alignment


def cell_string_single_line(string: str,
                            width: int,
                            padding: int,
                            align: Alignment,
                            trunc_value: str = "...") -> str:

    string = string.split("\n")[0]
    string = " ".join(string.split("\t"))

    if len(string) + (padding * 2) > width:
        slice_outer_index = width - ((padding * 2) + len(trunc_value))
        string = f"{string[0:slice_outer_index]}{trunc_value}"

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


def cell_string_multi_line(string: str,
                           width: int,
                           padding: int,
                           max_lines: Optional[int] = None,
                           trunc_value: str = "...") -> List[str]:

    return_string_array = []

    clean_string = " ".join(string.split("\t"))
    initial_string_array = clean_string.split("\n")

    reached_max_lines = False

    for initial_string_item in initial_string_array:

        word_string_array = initial_string_item.split(" ")
        character_count = 0
        current_line_array = []
        for word_string_index, word_string_item in enumerate(word_string_array):
            character_count += len(word_string_item)
            if character_count + (padding * 2) < width:
                current_line_array.append(word_string_item)
            else:
                if max_lines and len(return_string_array) == max_lines - 1:
                    current_line_array.append(word_string_item)
                    current_line_string = " ".join(current_line_array)
                    return_string_array.append(cell_string_single_line(string=current_line_string,
                                                                       width=width,
                                                                       padding=padding,
                                                                       align="left",
                                                                       trunc_value=trunc_value))
                    reached_max_lines = True
                    break
                else:
                    current_line_string = " ".join(current_line_array)
                    return_string_array.append(cell_string_single_line(string=current_line_string,
                                                                       width=width,
                                                                       padding=padding,
                                                                       align="left",
                                                                       trunc_value=trunc_value))
                    current_line_array = [word_string_item]
                    character_count = len(word_string_item)
            character_count += 1
        if reached_max_lines:
            break
        current_line_string = " ".join(current_line_array)
        return_string_array.append(cell_string_single_line(string=current_line_string,
                                                           width=width,
                                                           padding=padding,
                                                           align="left",
                                                           trunc_value=trunc_value))
    return return_string_array
