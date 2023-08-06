from textframe.characters.line_h import h_line
from textframe.characters.matrix_cross import cross_matrix
from textframe.typing import BorderType


def row_cross_line(divider: BorderType, v_line_list_top: list, v_line_list_bottom: list) -> str:

    """
    :param divider: BorderType
    :param v_line_list_top: [[col_width, BorderType]]
    :param v_line_list_bottom: [[col_width, BorderType]]
    :return: str
    """

    return_string = ""

    cumulative_top_count = 0
    cumulative_top = []
    for v_line_index in range(0, len(v_line_list_top),):
        cumulative_top_count += v_line_list_top[v_line_index][0]
        cumulative_top.append([v_line_list_top[v_line_index][0], cumulative_top_count, v_line_list_top[v_line_index][1]])
    cumulative_top.reverse()
    cumulative_bottom_count = 0
    cumulative_bottom = []
    for v_line_index in range(0, len(v_line_list_bottom)):
        cumulative_bottom_count += v_line_list_bottom[v_line_index][0]
        cumulative_bottom.append([v_line_list_bottom[v_line_index][0], cumulative_bottom_count, v_line_list_bottom[v_line_index][1]])
    cumulative_bottom.reverse()

    current_v_line_index = len(v_line_list_top) + len(v_line_list_bottom)

    while current_v_line_index > 0:
        if len(cumulative_top) > 0 and len(cumulative_bottom) > 0:
            if cumulative_top[-1][1] > cumulative_bottom[-1][1]:
                # return_string += "one"
                return_string += f"{h_line[divider] * cumulative_bottom[-1][0]}{cross_matrix['blank'][divider][cumulative_bottom[-1][2]]}"
                cumulative_top[-1][0] = cumulative_top[-1][0] - cumulative_bottom[-1][0] - 1
                cumulative_bottom.pop()
            elif cumulative_top[-1][1] == cumulative_bottom[-1][1]:
                # return_string += "two"
                return_string += f"{h_line[divider] * cumulative_bottom[-1][0]}{cross_matrix[cumulative_top[-1][2]][divider][cumulative_bottom[-1][2]]}"
                cumulative_top.pop()
                cumulative_bottom.pop()
            elif cumulative_top[-1][1] < cumulative_bottom[-1][1]:
                # return_string += "three"
                return_string += f"{h_line[divider] * cumulative_top[-1][0]}{cross_matrix[cumulative_top[-1][2]][divider]['blank']}"
                cumulative_bottom[-1][0] = cumulative_bottom[-1][0] - cumulative_top[-1][0] - 1
                cumulative_top.pop()
        else:
            if len(cumulative_top) > 0:
                return_string += f"{h_line[divider] * cumulative_top[-1][0]}{cross_matrix[cumulative_top[-1][2]][divider]['blank']}"
                if cumulative_top[-1][0] < 0:
                    return_string = return_string[0:cumulative_top[-1][0]]
                cumulative_top.pop()
            if len(cumulative_bottom) > 0:
                return_string += f"{h_line[divider] * cumulative_bottom[-1][0]}{cross_matrix['blank'][divider][cumulative_bottom[-1][2]]}"
                if cumulative_bottom[-1][0] < 0:
                    return_string = return_string[0:cumulative_bottom[-1][0]]
                cumulative_bottom.pop()
        current_v_line_index -= 1
    return return_string[0:-1]

