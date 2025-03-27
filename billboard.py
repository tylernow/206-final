from bs4 import BeautifulSoup
import re
import unittest
import os
import csv
import requests

"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"

An example of that within the function would be:
    open("filename", "r", encoding="utf-8-sig")

"""

def top_hundred_songs(): 
    """
    INPUT: none
    Returns: a dictionary called songs, where each song has a dictionary with an integer ranking value and a list of their artists
    """
    # make beautiful soup
    url = f"https://www.billboard.com/charts/hot-100/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # retrieve songs
    songs = {}
    tags = soup.find_all('div', class_='o-chart-results-list-row-container')
    for tag in tags:
        # song name
        data = tag.find()
        songName = ""
        if data:
            songName = data.text
        
        # song ranking
        data = tag.find()
        ranking = 0
        if data:
            ranking = int(data.text)
        
        # artists
        data = tag.find_all()
        artists = []
        if data:
            artists = data
        
        songs[songName] = {"ranking" : ranking, "artist(s)" : artists}

    return songs

def make_database(filename, data):
    """
    INPUT: filename to make database in, dictionary (from top_hundred_songs()) to send to database
    Returns: None
    """


class TestCases(unittest.TestCase):
    def test_top_hundred_songs(self):
        songs = top_hundred_songs()

        # check that there are 100 songs
        self.assertEqual(type(songs), dict)
        self.assertEqual(len(songs), 100)

        # check that each song has a valid name and ranking + artist
        prevRanking = 0
        for song, info in songs.items():
            self.assertGreater(len(song), 0)
            self.assertEqual(len(info), 2)

            # check for valid ranking
            ranking = info["ranking"]
            self.assertEqual(type(ranking), int)
            self.assertGreater(ranking, prevRanking)
            self.assertLessEqual(ranking, 100)
            prevRanking = ranking

            # check for valid artist names
            artists = info["artists"]
            self.assertEqual(type(artists), list)
            self.assertGreater(len(artists), 0)
            for artist in artists:
                self.assertEqual(type(artist), str)


def main (): 
    detailed_data = create_listing_database("html_files/search_results.html")
    output_csv(detailed_data, "airbnb_dataset.csv")

if __name__ == '__main__':
    # main()
    unittest.main(verbosity=2)