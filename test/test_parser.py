import pathlib
from unittest import TestCase

from main.parser import Top2000Parser, Top2000RankingDownloader


class Top2000TestRankingDownloader(Top2000RankingDownloader):

    def __init__(self):
        self.returnValue = pathlib.Path('top2000-2022.json').read_text()

    def download(self, url: str) -> str:
        return self.returnValue


class TestTop2000Parser(TestCase):

    def test_parse(self):
        parser = Top2000Parser(Top2000TestRankingDownloader())
        top2000_entries = parser.parse(2022)
        self.assertEqual(2000, len(top2000_entries))
        self.assertEqual("Queen", top2000_entries[0].artist)
        self.assertEqual("Bohemian Rhapsody", top2000_entries[0].song)
