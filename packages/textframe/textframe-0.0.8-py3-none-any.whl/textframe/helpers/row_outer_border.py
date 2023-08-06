from textframe.characters.line_v import v_line
from textframe.characters.matrix_side import left_side_matrix, right_side_matrix
from textframe.typing import BorderType


def row_outer_border(row_string: str, outer_border: BorderType, row_divider: BorderType = None) -> str:
    left_border = left_side_matrix[outer_border][row_divider] if row_divider else v_line[outer_border]
    right_border = right_side_matrix[outer_border][row_divider] if row_divider else v_line[outer_border]
    return f"{left_border}{row_string}{right_border}"
