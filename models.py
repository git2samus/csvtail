import csv


class CSV(object):
    def __init__(self, fname):
        #TODO get csv.reader arguments from commandline
        with open(fname) as f:
            # dump entire csv in memory (will figure out optimizations later)
            self.rows = tuple(csv.reader(f))

        # calculate maximum width of each column
        self.col_widths = []
        for row in self.rows:
            for field_i, field in enumerate(row):
                # grow list along with columns
                if len(self.col_widths) <= field_i:
                    self.col_widths.append(0)

                self.col_widths[field_i] = max(
                    self.col_widths[field_i], len(field)
                )
