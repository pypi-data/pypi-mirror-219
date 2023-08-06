from tablestring.TableString import TableString


x = TableString(width=150, border="thick")

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
        "Key One": "Blah",
        "Key Two": "Blah",
        "Key Three": "Blah"

    },
    {
        "Key One": "Blah dfsdfsdfsdfkksdlfkjsdljflsdkjflsdkjflsdkjflksdjflsdkjflsdkjflsdkjflksdjflkdsjflksdjflkdsjfs",
        "Key Two": "Blah",
        "Key Three": "Blah s.kflsdjlsdkjflsdkjf;lskdjf;lkdjfls;kdjfl;skdjfsl;kdjflds;kfjsl;kdjfl;sdkjflsd;kjf;slkdjf;sdlkjf"

    },
]

options = {
    "header_base_divider": "thick",
    "row_line_divider": "none",
    "column_divider": "thin",
    "header_column_divider": "none",
    "frame_base_divider": "thick",
    # "header_align": "center"
}

x.add_table_frame(column_list, row_list, options)

column_list2 = [
    {
        "key": "Key One",
        "width": 60,
        "align": "right"
    },
    {
        "key": "Key Two"
    },
    {
        "key": "Key Three"
    }
]
x.add_table_frame(column_list2, row_list, options)

x.print()

