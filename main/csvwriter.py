import csv
from typing import List

from main.parser import Top2000Entry


class Top2000CsvWriter:

    def write(self, year: int, top2000_entries: List[Top2000Entry]):
        if len(top2000_entries) <= 0:
            return
        attributes = top2000_entries[0].__dict__.keys()
        with open(f'data/top2000_{year}.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(attributes)
            for top2000_entry in top2000_entries:
                writer.writerow(top2000_entry.__dict__.values())