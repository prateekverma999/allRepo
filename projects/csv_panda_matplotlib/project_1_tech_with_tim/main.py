import pandas as pd # type: ignore
import csv
from datetime import datetime



class intiallize():
    csv_file = 'data.csv'

    @classmethod
    def read_csv(cls):
        try:
            df = pd.read_csv(cls.csv_file)
            return df
        except FileNotFoundError:
            df = pd.DataFrame(columns=['date', 'amount', 'category', 'description'])
            df.to_csv(cls.csv_file, index=False)

intiallize.read_csv()