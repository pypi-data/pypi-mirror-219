import textframe as tf

# x = tf.TextFrame(width=60, border="double")

# column_list = [
#     {
#         "key": "Key One",
#         "width":  20
#     },
#     {
#         "key": "Key Two"
#     },
#     {
#         "key": "Key Three"
#     }
# ]
#
# row_list = [
#     {
#         "Key One": "Blah",
#         "Key Two": "Blah",
#         "Key Three": "Blah"
#
#     },
#     {
#         "Key One": "Bla\nh",
#         "Key Two": "Blah",
#         "Key Three": "Blah"
#
#     },
#     {
#         "Key One": "Blah dfsdfsdfsdfkksdlfkjsdljflsdkjf\t\t\t\tlsdkjflsdkjflksdjflsdkjflsdkjflsdkjflksdjflkdsjflksdjflkdsjfs",
#         "Key Two": "B\nlah",
#         "Key Three": "Blah s.kflsdjlsdkjflsdkjf;lskdjf;lkdjfls;kdjfl;skdjfsl;kdjflds;kfjsl;kdjfl;sdkjflsd;kjf;slkdjf;sdlkjf"
#
#     },
# ]
#
# options = {
#     "header_base_divider": "thick",
#     "row_line_divider": "blank",
#     "column_divider": "thin",
#     "header_column_divider": "none",
#     "frame_base_divider": "thick",
#     # "header_align": "center"
# }
#
# x.add_table_frame(column_list, row_list, options)
# x.add_text_frame("This is my test", multiline=False)
#
#
# really_long_string = "kjslkjslkj\tdslkjlskdjf lkjl sdfklj sdklslk  ljlk lkdfjd\tslk kl lkfkds lk ds lkdslkj lk lk dslkjf\tdslkfslkfl kkl sdkldsfkljdsfkds lsdksdlkf  sdfkldskljdsfkls lskdfkl d"
# new_long_string = "slkjslkj\tdslkjlskdjf lkjl sdfklj sdklslk  ljlk lkdfjd\tslk kl lkfkds lk ds lkdslkj lk lk dslkjf\tdslkfslkfl kkl sdkldsfkljdsfkds lsdksdlkfs kll\tks  sdfkldskljdsfkls slkjslkj\tdslkjlskdjf lkjl sdfklj sdklslk  ljlk lkdfjd\tslk kl lkfkds lk ds lkdslkj lk lk dslkjf\tdslkfslkfl kkl sdkldsfkljdsfkds lsdksdlkfs kll\tks  sdfkldskljdsfkls slkjslkj\tdslkjlskdjf lkjl sdfklj sdklslk  ljlk lkdfjd\tslk kl lkfkds lk ds lkdslkj lk lk dslkjf\tdslkfslkfl kkl sdkldsfkljdsfkds lsdksdlkfs kll\tks  sdfkldskljdsfkls slkjslkj\tdslkjlskdjf lkjl sdfklj sdklslk  ljlk lkdfjd\tslk kl lkfkds lk ds lkdslkj lk lk dslkjf\tdslkfslkfl kkl sdkldsfkljdsfkds lsdksdlkfs kll\tks  sdfkldskljdsfkls slkjslkj\tdslkjlskdjf lkjl sdfklj sdklslk  ljlk lkdfjd\tslk kl lkfkds lk ds lkdslkj lk lk dslkjf\tdslkfslkfl kkl sdkldsfkljdsfkds lsdksdlkfs kll\tks  sdfkldskljdsfkls slkjslkj\tdslkjlskdjf lkjl sdfklj sdklslk  ljlk lkdfjd\tslk kl lkfkds lk ds lkdslkj lk lk dslkjf\tdslkfslkfl kkl sdkldsfkljdsfkds lsdksdlkfs kll\tks  sdfkldskljdsfkls slkjslkj\tdslkjlskdjf lkjl sdfklj sdklslk  ljlk lkdfjd\tslk kl lkfkds lk ds lkdslkj lk lk dslkjf\tdslkfslkfl kkl sdkldsfkljdsfkds lsdksdlkfs kll\tks  sdfkldskljdsfkls "
#
# x.add_text_frame(really_long_string, multiline=False)
# x.add_text_frame(really_long_string, multiline=False)
#
# x.add_text_frame(really_long_string)
# x.add_text_frame(new_long_string)
#
# x.add_text_frame(new_long_string, max_lines=3)
#
#
# column_list2 = [
#     {
#         "key": "Key One",
#         "width": 60,
#         "align": "right"
#     },
#     {
#         "key": "Key Two"
#     },
#     {
#         "key": "Key Three"
#     }
# ]
#
# options2 = {
#     "header_base_divider": "thick",
#     "row_line_divider": "blank",
#     "column_divider": "thin",
#     "header_column_divider": "none",
#     "frame_base_divider": "thick",
#     # "header_align": "center"
# }
# x.add_table_frame(column_list2, row_list, options2)
#
# x.print()
#
# column_list3 = [
#     {
#         "key": "Key One",
#         "align": "left"
#     },
# ]
#
# options3 = {
#     "header_base_divider": "thick",
#     "row_line_divider": "thin",
#     "column_divider": "thin",
#     "header_column_divider": "thick",
#     "frame_base_divider": "none",
#     "text_padding": 4
#     # "header_align": "center"
# }
#
# x.add_table_frame(column_list3, row_list, options3)
#
# column_list4 = [
#     {
#         "key": "Key One",
#         "width": 60,
#         "align": "right"
#     },
#     {
#         "key": "Key Two"
#     },
# ]
# x.add_table_frame(column_list4, row_list, options3)
#
# column_list5 = [
#     {
#         "key": "Key One",
#         "width": 60,
#         "align": "right"
#     },
#     {
#         "key": "Key Two"
#     },
#     {
#         "key": "Key One",
#         "align": "right"
#     },
#     {
#         "key": "Key Two"
#     },
#     {
#         "key": "Key One",
#         "align": "right"
#     },
#     {
#         "key": "Key Two"
#     },
# ]
#
# x.add_table_frame(column_list5, row_list, options3)
#
#
#
#
# x.print()
#
#
# really_really_long_string = "kjslkjslkj\t dslkjlskdjf lkjl sdfklj sdklslk  ljlk lkdfjd\t slk kl lkfkds lk ds l\nkdslkj lk lk dslkjf\tdslkfslkfl kkl sdkldsf\nkljdsfkds lsdksdlkfs kll\tks  sdfkldskljdsfkls lskdfkl d"
#
# x.add_text_frame(really_really_long_string, multiline=True)
# x.print()


column_list = [
    {
        "key": "Key One",
        "width":  20
    },
    {
        "key": "Key Two"
    },
    {
        "key": "Key Three"
    }
]

row_list = [
    {
        "Key One": "Blah",
        "Key Two": "Blah",
        "Key Three": "Blah"

    },
    {
        "Key One": "Bla\nh",
        "Key Two": "Blah",
        "Key Three": "Blah"

    },
    {
        "Key One": "Blah dfsdfsdfsdfkksdlfkjsdljflsdkjf\t\t\t\tlsdkjflsdkjflksdjflsdkjflsdkjflsdkjflksdjflkdsjflksdjflkdsjfs",
        "Key Two": "B\nlah",
        "Key Three": "Blah s.kflsdjlsdkjflsdkjf;lskdjf;lkdjfls;kdjfl;skdjfsl;kdjflds;kfjsl;kdjfl;sdkjflsd;kjf;slkdjf;sdlkjf"

    },
    {
        "Key One": "Blah",
        "Key Two": "Blah",
        "Key Three": "Blah"

    },
    {
        "Key One": "Bla\nh",
        "Key Two": "Blah",
        "Key Three": "Blah"

    },
    {
        "Key One": "Blah dfsdfsdfsdfkksdlfkjsdljflsdkjf\t\t\t\tlsdkjflsdkjflksdjflsdkjflsdkjflsdkjflksdjflkdsjflksdjflkdsjfs",
        "Key Two": "B\nlah",
        "Key Three": "Blah s.kflsdjlsdkjflsdkjf;lskdjf;lkdjfls;kdjfl;skdjfsl;kdjflds;kfjsl;kdjfl;sdkjflsd;kjf;slkdjf;sdlkjf"

    },
    {
        "Key One": "Blah",
        "Key Two": "Blah",
        "Key Three": "Blah"

    },
    {
        "Key One": "Bla\nh",
        "Key Two": "Blah",
        "Key Three": "Blah"

    },
    {
        "Key One": "Blah dfsdfsdfsdfkksdlfkjsdljflsdkjf\t\t\t\tlsdkjflsdkjflksdjflsdkjflsdkjflsdkjflksdjflkdsjflksdjflkdsjfs",
        "Key Two": "B\nlah",
        "Key Three": "Blah s.kflsdjlsdkjflsdkjf;lskdjf;lkdjfls;kdjfl;skdjfsl;kdjflds;kfjsl;kdjfl;sdkjflsd;kjf;slkdjf;sdlkjf"

    },
    {
        "Key One": "Blah",
        "Key Two": "Blah",
        "Key Three": "Blah"

    },
    {
        "Key One": "Bla\nh",
        "Key Two": "Blah",
        "Key Three": "Blah"

    },
    {
        "Key One": "Blah dfsdfsdfsdfkksdlfkjsdljflsdkjf\t\t\t\tlsdkjflsdkjflksdjflsdkjflsdkjflsdkjflksdjflkdsjflksdjflkdsjfs",
        "Key Two": "B\nlah",
        "Key Three": "Blah s.kflsdjlsdkjflsdkjf;lskdjf;lkdjfls;kdjfl;skdjfsl;kdjflds;kfjsl;kdjfl;sdkjflsd;kjf;slkdjf;sdlkjf"

    },
]
options = {
    "row_line_divider": "thin"
}
# x.add_table_frame(column_list, row_list, options)
# x.print()

# print_string = x.to_string()
# print(print_string)

new_frame = tf.TextFrame(width=300)
new_frame.add_table_frame(column_list, row_list, options)
new_frame.print()