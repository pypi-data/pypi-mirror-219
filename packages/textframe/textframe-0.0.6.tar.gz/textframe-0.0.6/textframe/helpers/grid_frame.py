def grid_row():

    # needs to return all sorts of useful info (necessary for header... like column widths all calculated)



    min_column_width = (text_padding * 2) + 1
    total_column_width = 0
    total_defined_column_width = 0
    calculated_width_columns = []

    for column_index, column_item in enumerate(columns):
        if "width" in column_item:
            if column_item["width"] < min_column_width:
                raise Exception(
                    f"Column '{column_item['key']}' has a width ({column_item['width']}) less than minimum column width ({min_column_width}).")
            total_defined_column_width += column_item["width"]
        else:
            calculated_width_columns.append(column_index)

    if len(calculated_width_columns) > 0:
        calculated_width_total = self._outer_width - (total_defined_column_width + len(columns) + 1)
        calculated_column_width = math.floor((calculated_width_total / len(calculated_width_columns)))
        if calculated_column_width < min_column_width:
            raise Exception(
                f"Calculated column width ({calculated_column_width}) is less than minimum column width ({min_column_width}).")
        for column_index, column_item in enumerate(columns):
            if column_index in calculated_width_columns:
                column_item["width"] = calculated_column_width
            total_column_width += column_item["width"]
    else:
        total_column_width = total_defined_column_width

    if total_column_width + len(columns) + 1 > self._outer_width:
        raise Exception(
            f"Table width exceeds '{TextFrame.__name__}' width by {total_column_width - self._outer_width}.")
    if total_column_width + len(columns) + 1 < self._outer_width:
        if len(calculated_width_columns) > 0:
            columns[calculated_width_columns[0]]["width"] += (self._outer_width - total_column_width) - (
                        len(columns) + 1)
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
