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
    OUTPUT: a dictionary called songs, where each song has a dictionary with an integer ranking value and a list of their artists
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
