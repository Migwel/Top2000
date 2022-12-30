import pathlib
from unittest import TestCase

from main.parser import Top2000RankingDownloader, Top2000Processor
from main.writer import Top2000DatabaseWriter


class Top2000TestRankingDownloader(Top2000RankingDownloader):

    def __init__(self):
        self.returnValue = pathlib.Path('top2000-2022.json').read_text()

    def download(self, url: str) -> str:
        return self.returnValue


class Top2000TestRankingErrorDownloader(Top2000RankingDownloader):

    def __init__(self):
        self.returnValue = pathlib.Path('top2000-error.json').read_text()

    def download(self, url: str) -> str:
        return self.returnValue


class Top2000TestRankingValidDownloader(Top2000RankingDownloader):

    def __init__(self):
        self.nb_calls = 0
        self.returnValidValue = pathlib.Path('top2000-bohemianrhapsody.json').read_text()
        self.returnErrorValue = pathlib.Path('top2000-error.json').read_text()

    def download(self, url: str) -> str:
        if self.nb_calls == 0:
            self.nb_calls += 1
            return self.returnValidValue

        return self.returnErrorValue


class TestTop2000Processor(TestCase):

    def test_downloadRankings_valid(self):
        processor = Top2000Processor(Top2000TestRankingValidDownloader())
        rankings = processor.downloadRankings()
        self.assertEqual(24, len(rankings))
        ranking_2022 = rankings["2022"]
        first_position_2022 = ranking_2022.entries[0]
        self.assertEqual("Queen", first_position_2022.artist)
        self.assertEqual("Bohemian Rhapsody", first_position_2022.song)
        self.assertEqual(1975, first_position_2022.year)
        writer = Top2000DatabaseWriter()
        for year, ranking in rankings.items():
            writer.write(year, ranking)

    def test_downloadRankings_error(self):
        processor = Top2000Processor(Top2000TestRankingErrorDownloader())
        rankings = processor.downloadRankings()
        self.assertEqual(0, len(rankings))
