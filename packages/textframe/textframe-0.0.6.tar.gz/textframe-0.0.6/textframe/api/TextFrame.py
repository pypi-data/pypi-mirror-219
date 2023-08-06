import math
import shutil
import time
from typing import List, Dict

from textframe.characters.corners import top_left, top_right, bottom_left, bottom_right
from textframe.characters.line_v import v_line
from textframe.helpers.is_last_element import is_last_element
from textframe.helpers.row_frame_divider import row_frame_divider
from textframe.helpers.row_outer_border import row_outer_border
from textframe.helpers.cell_string import cell_string_single_line, cell_string_multi_line
from textframe.typing import BorderType, TableFrameColumnDict, TableFrameOption


class TextFrame:

    _border: BorderType
    _left_padding: int
    _outer_width: 1
    _frame_divider: BorderType

    _output_frame_list = []

    def __init__(self,
                 border: BorderType = "thick",
                 width: int = None,
                 left_padding: int = 1,
                 frame_divider: BorderType = "thick"):
        self._border = border if border != 'none' else 'blank'
        self._outer_width = width if width else shutil.get_terminal_size((120 + (left_padding * 2), 0))[0] - (left_padding * 2)
        self._left_padding = left_padding
        self._frame_divider = frame_divider

    def add_text_frame(self, text: str, multiline: bool = True, max_lines: int | None = None, options=None):
        line_strings_array = []
        if multiline:
            multiline_array = cell_string_multi_line(string=text,
                                                     width=self._outer_width - 2,
                                                     padding=1,
                                                     max_lines=max_lines)
            for multiline_item in multiline_array:
                line_strings_array.append(row_outer_border(row_string=multiline_item,
                                                           outer_border=self._border))
        else:
            row_string_inner = cell_string_single_line(string=text,
                                                       width=self._outer_width - 2,
                                                       padding=1,
                                                       align="left",
                                                       trunc_value="...")
            line_strings_array.append(row_outer_border(row_string=row_string_inner,
                                                       outer_border=self._border))

        self._output_frame_list.append({
            "v_lines": [[self._outer_width - 2, "blank"]],
            "line_strings": line_strings_array,
            "base_divider": self._frame_divider,
        })

    # def add_grid_frame(self, text: str, multiline: bool, options):
    #     min_column_width = (text_padding * 2) + 1
    #     total_column_width = 0
    #     total_defined_column_width = 0
    #     calculated_width_columns = []
    #
    #     for column_index, column_item in enumerate(columns):
    #         if "width" in column_item:
    #             if column_item["width"] < min_column_width:
    #                 raise Exception(
    #                     f"Column '{column_item['key']}' has a width ({column_item['width']}) less than minimum column width ({min_column_width}).")
    #             total_defined_column_width += column_item["width"]
    #         else:
    #             calculated_width_columns.append(column_index)
    #
    #     if len(calculated_width_columns) > 0:
    #         calculated_width_total = self._outer_width - (total_defined_column_width + len(columns) + 1)
    #         calculated_column_width = math.floor((calculated_width_total / len(calculated_width_columns)))
    #         if calculated_column_width < min_column_width:
    #             raise Exception(
    #                 f"Calculated column width ({calculated_column_width}) is less than minimum column width ({min_column_width}).")
    #         for column_index, column_item in enumerate(columns):
    #             if column_index in calculated_width_columns:
    #                 column_item["width"] = calculated_column_width
    #             total_column_width += column_item["width"]
    #     else:
    #         total_column_width = total_defined_column_width
    #
    #     if total_column_width + len(columns) + 1 > self._outer_width:
    #         raise Exception(
    #             f"Table width exceeds '{TextFrame.__name__}' width by {total_column_width - self._outer_width}.")
    #     if total_column_width + len(columns) + 1 < self._outer_width:
    #         if len(calculated_width_columns) > 0:
    #             columns[calculated_width_columns[0]]["width"] += (self._outer_width - total_column_width) - (
    #                         len(columns) + 1)
    #         else:
    #             raise Exception(
    #                 f"Table width exceeds '{TextFrame.__name__}' width by {total_column_width - self._outer_width}.")
    #
    #     header_v_lines = []
    #     row_v_lines = []
    #     width_tally = 0
    #
    #     for column_index, column_item in enumerate(columns):
    #         if column_index < len(columns):
    #             width_tally += column_item["width"]
    #             header_v_lines.append([column_item["width"], header_column_divider])
    #             row_v_lines.append([column_item["width"], row_column_divider])
    #
    #     header_line_string = ""
    #
    #     for column_index, column_item in enumerate(columns):
    #
    #         if "header_align" in options:
    #             header_align = options["header_align"]
    #         elif "align" in column_item:
    #             header_align = column_item["align"]
    #         else:
    #             header_align = "left"
    #
    #         header_line_string += cell_string_single_line(string=column_item["key"],
    #                                                       width=column_item["width"],
    #                                                       padding=text_padding,
    #                                                       align=header_align,
    #                                                       trunc_value=".")
    #
    #         if not is_last_element(column_index, columns):
    #             header_line_string += v_line[header_column_divider]
    #
    #     self._output_frame_list.append({
    #         "v_lines": header_v_lines,
    #         "line_strings": [row_outer_border(row_string=header_line_string, outer_border=self._border)],
    #         "base_divider": header_base_divider,
    #     })

    def add_table_frame(self,
                        columns: List[TableFrameColumnDict],
                        rows: List[Dict[str, str | int | float]],
                        options: TableFrameOption = None):


        options = {} if not options else options

        row_column_divider = options["column_divider"] if "column_divider" in options else "thin"
        row_column_divider = "blank" if row_column_divider == "none" else row_column_divider
        row_line_divider = options["row_line_divider"] if "row_line_divider" in options else "thin"
        header_column_divider = options["header_column_divider"] if "header_column_divider" in options else row_column_divider
        header_column_divider = "blank" if header_column_divider == "none" else header_column_divider
        header_base_divider = options["header_base_divider"] if "header_base_divider" in options else header_column_divider
        text_padding = options["text_padding"] if "text_padding" in options else 1
        frame_divider = options["frame_base_divider"] if "frame_base_divider" in options else self._frame_divider

        min_column_width = (text_padding * 2) + 1
        total_column_width = 0
        total_defined_column_width = 0
        calculated_width_columns = []

        for column_index, column_item in enumerate(columns):
            if "width" in column_item:
                if column_item["width"] < min_column_width:
                    raise Exception(f"Column '{column_item['key']}' has a width ({column_item['width']}) less than minimum column width ({min_column_width}).")
                total_defined_column_width += column_item["width"]
            else:
                calculated_width_columns.append(column_index)

        if len(calculated_width_columns) > 0:
            calculated_width_total = self._outer_width - (total_defined_column_width + len(columns) + 1)
            calculated_column_width = math.floor((calculated_width_total / len(calculated_width_columns)))
            if calculated_column_width < min_column_width:
                raise Exception(f"Calculated column width ({calculated_column_width}) is less than minimum column width ({min_column_width}).")
            for column_index, column_item in enumerate(columns):
                if column_index in calculated_width_columns:
                    column_item["width"] = calculated_column_width
                total_column_width += column_item["width"]
        else:
            total_column_width = total_defined_column_width

        if total_column_width + len(columns) + 1 > self._outer_width:
            raise Exception(f"Table width exceeds '{TextFrame.__name__}' width by {total_column_width - self._outer_width}.")
        if total_column_width + len(columns) + 1 < self._outer_width:
            if len(calculated_width_columns) > 0:
                columns[calculated_width_columns[0]]["width"] += (self._outer_width - total_column_width) - (len(columns) + 1)
            else:
                raise Exception(
                    f"Table width exceeds '{TextFrame.__name__}' width by {total_column_width - self._outer_width}.")

        header_v_lines = []
        row_v_lines = []
        width_tally = 0

        for column_index, column_item in enumerate(columns):
            if column_index < len(columns):
                width_tally += column_item["width"]
                header_v_lines.append([column_item["width"], header_column_divider])
                row_v_lines.append([column_item["width"], row_column_divider])

        header_line_string = ""

        for column_index, column_item in enumerate(columns):

            if "header_align" in options:
                header_align = options["header_align"]
            elif "align" in column_item:
                header_align = column_item["align"]
            else:
                header_align = "left"

            header_line_string += cell_string_single_line(string=column_item["key"],
                                                          width=column_item["width"],
                                                          padding=text_padding,
                                                          align=header_align,
                                                          trunc_value=".")

            if not is_last_element(column_index, columns):
                header_line_string += v_line[header_column_divider]

        self._output_frame_list.append({
            "v_lines": header_v_lines,
            "line_strings": [row_outer_border(row_string=header_line_string, outer_border=self._border)],
            "base_divider": header_base_divider,
        })

        start = time.perf_counter_ns()


        row_line_strings_list = []
        line_string = None

        if row_line_divider != "none":
            line_string = row_frame_divider(divider=row_line_divider,
                                            v_line_list_top=row_v_lines,
                                            v_line_list_bottom=row_v_lines)
        for row_index, row_item in enumerate(rows):
            row_line_string = ""
            for column_index, column_item in enumerate(columns):
                if "align" in column_item:
                    column_align = column_item["align"]
                else:
                    column_align = "left"
                row_line_string += cell_string_single_line(string=row_item[column_item["key"]],
                                                           width=column_item["width"],
                                                           padding=text_padding,
                                                           align=column_align,
                                                           trunc_value="...")
                if not is_last_element(column_index, columns):
                    row_line_string += v_line[row_column_divider]
            row_line_strings_list.append(row_outer_border(row_string=row_line_string, outer_border=self._border))
            if not is_last_element(row_index, rows) and line_string:
                row_line_strings_list.append(row_outer_border(row_string=line_string,
                                                              outer_border=self._border,
                                                              row_divider=row_line_divider))
        if row_line_divider == "blank":
            row_line_strings_list.insert(0, row_outer_border(row_string=line_string, outer_border=self._border))
            row_line_strings_list.append(row_outer_border(row_string=line_string,
                                                          outer_border=self._border,
                                                          row_divider=row_line_divider))

        self._output_frame_list.append({
            "v_lines": row_v_lines,
            "line_strings": row_line_strings_list,
            "base_divider": frame_divider,
        })

        end = time.perf_counter_ns()

        print("add_table_frame()", end - start)

    def to_string(self):

        start = time.perf_counter_ns()

        return_string = ""
        top_border_inner = row_frame_divider(divider=self._border,
                                             v_line_list_top=[],
                                             v_line_list_bottom=self._output_frame_list[0]["v_lines"])
        return_string += f"{' ' * self._left_padding}{top_left[self._border]}{top_border_inner}{top_right[self._border]}\n"
        for frame_index, frame_item in enumerate(self._output_frame_list):
            for row_index, row_item in enumerate(frame_item["line_strings"]):
                return_string += f"{' ' * self._left_padding}{row_item}\n"
            if not is_last_element(frame_index, self._output_frame_list):
                if self._output_frame_list[frame_index]['base_divider'] != 'none':
                    frame_divider_inner = row_frame_divider(divider=self._output_frame_list[frame_index]['base_divider'],
                                                            v_line_list_top=self._output_frame_list[frame_index]["v_lines"],
                                                            v_line_list_bottom=self._output_frame_list[frame_index + 1]["v_lines"])
                    frame_divider_outer = row_outer_border(row_string=frame_divider_inner,
                                                           outer_border=self._border,
                                                           row_divider=self._output_frame_list[frame_index]['base_divider'])
                    return_string += f"{' ' * self._left_padding}{frame_divider_outer}\n"
        bottom_border_inner = row_frame_divider(divider=self._border,
                                                v_line_list_top=self._output_frame_list[-1]["v_lines"],
                                                v_line_list_bottom=[])
        return_string += f"{' ' * self._left_padding}{bottom_left[self._border]}{bottom_border_inner}{bottom_right[self._border]}\n"

        end = time.perf_counter_ns()
        print("to_string()", end - start)

        return return_string

    def print(self):
        print_string = self.to_string()
        start = time.perf_counter_ns()
        print(print_string)
        end = time.perf_counter_ns()
        print("print()", end - start)
