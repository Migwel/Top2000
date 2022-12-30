import json

import requests as requests


class Top2000Ranking:
    def __init__(self, year):
        self.year = year
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)


class Top2000Entry:
    def __init__(self,
                 position : int,
                 artist: str,
                 song: str,
                 year: int):
        self.position = position
        self.artist = artist
        self.song = song
        self.year = year


class Top2000RankingDownloader:

    def download(self, url: str) -> str:
        page = requests.get(url)
        return page.text


class Top2000Processor:

    def __init__(self, downloader: Top2000RankingDownloader, errors_allowed = 0):
        self.downloader = downloader
        self.errors_allowed = errors_allowed

    def downloadRankings(self):
        track_id = 4620
        nb_errors = 0
        rankings = {}
        while True:
            url = f"https://www.nporadio2.nl/api/statistics/positions/track/{track_id}"
            track_statistics_json = self.downloader.download(url)
            track_statistics = json.loads(track_statistics_json)
            if not isinstance(track_statistics, list):
                print(f"Skipping track {track_id}")
                nb_errors += 1
                if nb_errors > self.errors_allowed:
                    break
                else:
                    track_id += 1
                    continue

            nb_errors = 0
            print(f"Getting track {track_id}")
            for track_year_ranking in track_statistics:
                if track_year_ranking.get("position") is None:
                    continue

                year = str(track_year_ranking["name"])
                entry = Top2000Entry(track_year_ranking["position"],
                                     track_year_ranking["artist"],
                                     track_year_ranking["title"],
                                     track_year_ranking["release_year"])

                year_ranking = rankings.get(year, Top2000Ranking(year))
                year_ranking.add_entry(entry)
                rankings[year] = year_ranking

            track_id += 1
        return rankings
