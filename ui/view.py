class ScrollOffsetException(Exception):
    pass


class View(object):
    RETURN_SYMBOL = "\u23CE"

    def __init__(self, csv_model):
        self.csv_model = csv_model
        # row and col from which the CSV should start printing
        self.row_offset, self.col_offset = 0, 0

    def scroll_up(self, offset=1):
        if self.row_offset - offset < 0:
            raise ScrollOffsetException

        self.row_offset -= offset

    def scroll_down(self, offset=1):
        if self.row_offset + offset >= len(self.csv_model.rows):
            raise ScrollOffsetException

        self.row_offset += offset

    def scroll_left(self, offset=1):
        if self.col_offset - offset < 0:
            raise ScrollOffsetException

        self.col_offset -= offset

    def scroll_right(self, offset=1):
        if self.col_offset + offset >= len(self.csv_model.col_widths):
            raise ScrollOffsetException

        self.col_offset += offset

    def format_field(self, csv_field_i, csv_field):
        #TODO color \n replacements
        field = csv_field.replace("\n", View.RETURN_SYMBOL)

        csv_col_widths = self.csv_model.col_widths
        colwidth = csv_col_widths[csv_field_i + self.col_offset]

        result = '{{field:>{colwidth}}}'
        result = result.format(colwidth=colwidth)
        result = result.format(field=field)

        return result

    def render(self, window):
        # measure window
        w_height, w_width = window.getmaxyx()

        # clear screen and mark for refresh
        window.clear()

        # rows from CSV that are visible
        row_slice = slice(self.row_offset, self.row_offset + w_height)

        csv_rows = self.csv_model.rows
        for w_row_i, csv_row in enumerate(csv_rows[row_slice]):
            # pad each visible field to optimum width and create grid
            rowtext = (
                self.format_field(csv_field_i, csv_field)
                for csv_field_i, csv_field
                in enumerate(csv_row[self.col_offset:])
            )
            rowtext = '|'.join(rowtext)
            rowtext = '|{}|'.format(rowtext)

            # draw a line (no longer than the terminal's width)
            window.addnstr(w_row_i, 0, rowtext, w_width)
