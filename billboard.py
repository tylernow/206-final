from bs4 import BeautifulSoup
import re
import unittest
import os
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
        # song ranking
        data = tag.find('span', class_='c-label')
        ranking = 0
        if data:
            ranking = int(data.text)

        tag = tag.find('ul', class_='lrv-a-unstyle-list lrv-u-flex lrv-u-height-100p lrv-u-flex-direction-column@mobile-max')
        # song name
        data = tag.find('h3', class_='c-title')
        songName = ""
        if data:
            songName = data.text.strip('\n\t')

        # artists
        data = tag.find('span', class_='c-label')
        artists = []
        if data:
            result = re.split(r'\s*FEATURING\s*|,\s*|&\s*', data.text.strip('\n\t'))
            for artist in result:
                artists.append(artist.rstrip())
        
        songs[songName] = {"ranking" : ranking, "artists" : artists}

    return songs

def make_database(filename, data):
    """
    INPUT: filename to make database in, dictionary (from top_hundred_songs()) to send to database
    Returns: None
    """
    pass


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
        
        # look at all songs
        print("----")
        for song, data in songs.items():
            print(f"{song} --> {data}")


def main (): 
    make_database("billboardTopSongs", top_hundred_songs())

if __name__ == '__main__':
    # main()
    unittest.main(verbosity=2)
