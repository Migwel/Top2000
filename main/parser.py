import json
from typing import List

import requests as requests

class Top2000Entry:
    def __init__(self,
                 current_position : int,
                 last_year_position : int,
                 artist: str,
                 artist_normalized : str,
                 song: str,
                 song_normalized: str):
        self.current_position = current_position
        self.last_year_position = last_year_position
        self.artist = artist
        self.artist_normalized = artist_normalized
        self.song = song
        self.song_normalized = song_normalized


class Top2000RankingDownloader:

    def download(self, url: str) -> str:
        page = requests.get(url)
        return page.text


class Top2000Parser:

    def __init__(self, downloader : Top2000RankingDownloader):
        self.downloader = downloader

    def parse(self, year: int) -> List[Top2000Entry]:
        url = f"https://www.nporadio2.nl/api/charts/top-2000-van-{year}-12-25"
        print(url)
        year_ranking_json = self.downloader.download(url)
        year_ranking = json.loads(year_ranking_json)
        top2000_entries = list()
        for entry in year_ranking["positions"]:
            top2000_entry = Top2000Entry(entry["position"]["current"],
                                         entry["position"]["previous"],
                                         entry["track"]["artist"],
                                         entry["track"]["artistNormalized"],
                                         entry["track"]["title"],
                                         entry["track"]["titleNormalized"])
            top2000_entries.append(top2000_entry)

        return top2000_entries