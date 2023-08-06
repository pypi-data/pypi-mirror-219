from typing import Literal, TypedDict

BorderType = Literal["none", "blank", "thin", "thick", "double"]
Alignment = Literal["left", "center", "right"]


# WidthOptions = int


class MinTableFrameColumnDict(TypedDict):
    key: str


class TableFrameColumnDict(MinTableFrameColumnDict, total=False):

    width: int
    align: Alignment


# class MinTableFrameRowDict(TypedDict):
#     value: str
#
#
# class TableFrameRowDict(MinTableFrameRowDict, total=False):
#     pass


class BaseFrameOption(TypedDict, total=False):
    text_padding: int
    frame_base_divider: BorderType


class TableFrameOption(BaseFrameOption, total=False):
    header_align: Alignment
    row_line_divider: BorderType
    column_divider: BorderType
    header_column_divider: BorderType
    header_base_divider: BorderType
    hide_header: bool
