import configparser
import csv
import sqlite3
from sqlite3 import Error
from typing import List

from main.parser import Top2000Entry, Top2000Ranking


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


class Top2000DatabaseWriter:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.properties")
        self.dbname = config["Sqlite"]["dbname"]

    def write(self, year: int, ranking: Top2000Ranking):
        if len(ranking.entries) <= 0:
            return

        try:
            connection = sqlite3.connect(self.dbname)
        except Error:
            return

        cursor = connection.cursor()
        self.init_tables(cursor)
        for top2000_entry in ranking.entries:
            self.add_entry(cursor, year, top2000_entry)
        connection.commit()
        connection.close()

    def init_tables(self, cursor):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entry (
          id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
          artist VARCHAR NOT NULL,
          song VARCHAR NOT NULL,
          year INTEGER NULL,
          UNIQUE (artist, song)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ranking (
          year INTEGER NOT NULL,
          position INTEGER NOT NULL,
          entry_id INTEGER NOT NULL,
          UNIQUE (year, position)
        )
        """)

    def add_entry(self, cursor, year, top2000_entry):
        cursor.execute("""
        INSERT INTO entry (artist, song, year) VALUES (?, ?, ?) ON CONFLICT (artist, song) DO NOTHING
        """, [top2000_entry.artist, top2000_entry.song, top2000_entry.year])
        cursor.execute("""
        INSERT INTO ranking (year, position, entry_id) select ?, ?, id from entry where artist = ? and song = ? ON CONFLICT (year, position) DO NOTHING
        """, [year, top2000_entry.position, top2000_entry.artist, top2000_entry.song])
