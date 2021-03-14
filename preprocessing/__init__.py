from os import sep
import pandas as pd


class InvalidDataException(Exception):
    pass

class DataPreview:
    def __init__(self, file):
        try:
            self.data = pd.read_csv(file, sep=",")
        except Exception as e:
            print(e)
            raise InvalidDataException()

    def get_column_names(self):
        return [ column for column in self.data.columns ] 

    def parse_single_row(self, row, columns):
        return { column: row[column] for column in columns }

    def parse_all_rows(self, dataframe, columns):
        rows = []

        for _, row in dataframe.iterrows():
            rows.append(self.parse_single_row(row, columns))

        return rows

    def get_first_5_rows(self):
        return self.data.head(5)

    def get_last_5_rows(self):
        return self.data.tail(5)

    def parse(self):
        first_5_rows = self.get_first_5_rows()
        last_5_rows = self.get_last_5_rows()
        columns = self.get_column_names()

        first_5_rows_as_json = self.parse_all_rows(first_5_rows, columns)
        last_5_rows_as_json = self.parse_all_rows(last_5_rows, columns)

        return {
            "headers": columns,
            "first_5": first_5_rows_as_json,
            "last_5": last_5_rows_as_json
        }




