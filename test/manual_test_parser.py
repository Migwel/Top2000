from unittest import TestCase

from main.parser import Top2000RankingDownloader, Top2000Processor
from main.writer import Top2000DatabaseWriter


class ManualTestTop2000Processor(TestCase):

    def test_downloadRankings_valid(self):
        processor = Top2000Processor(Top2000RankingDownloader(), 1000)
        rankings = processor.downloadRankings()
        writer = Top2000DatabaseWriter()
        for year, ranking in rankings.items():
            writer.write(year, ranking)