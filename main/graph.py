import configparser
import sqlite3
from sqlite3 import Error

from matplotlib import pyplot as plt


class YearPopularity:
    def __init__(self, ranking_year):
        self.ranking_year = ranking_year
        self.year_popularity = {}

    def add_year_popularity(self, key, value):
        self.year_popularity[key] = value


class GraphDrawer:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.properties")
        self.dbname = config["Sqlite"]["dbname"]

    def plot_year_popularity(self):
        try:
            connection = sqlite3.connect(self.dbname)
        except Error:
            return

        fig, ax = plt.subplots()
        for i in range(0, 3):
            for year in range(1999, 2023):
                cursor = connection.cursor()
                year_popularity = YearPopularity(year)
                cursor.execute("SELECT (e.year/10)*10, count(*) from ranking r join entry e on r.entry_id = e.id where r.year = ? group by 1", [year])
                for result in cursor.fetchall():
                    year_popularity.add_year_popularity(result[0], result[1])

                ax.bar(year_popularity.year_popularity.keys(), year_popularity.year_popularity.values())
                ax.set_xticks(range(1930, 2030, 10))
                ax.set_xlim(left=1920, right=2030)
                ax.set_yticks(range(0, 900, 100))
                ax.set_ylim(bottom=0, top=900)
                plt.title(year)
                fig.canvas.draw()
                pause = 0.5
                if year == 1999 or year == 2022:
                    pause = 2
                plt.pause(pause)
                plt.cla()
