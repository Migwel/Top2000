from unittest import TestCase

from main.csvwriter import Top2000CsvWriter
from main.parser import Top2000Parser, Top2000RankingDownloader


class ManualTestTop2000Parser(TestCase):

    def test_parse(self):
        parser = Top2000Parser(Top2000RankingDownloader())
        csv_writer = Top2000CsvWriter()
        for year in range(1999, 2023):
            top2000_entries = parser.parse(year)
            csv_writer.write(year, top2000_entries)
