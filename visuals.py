import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt

def connect_to_music_data():
    """
    Sets up a SQLite database connection and cursor to music_data.

    Parameters - NONE

    Returns - Tuple (cursor, connection)

    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def graph_rank_vs_popularity():
    """
    Graph Billboard rank vs Spotify popularity.
    """
    pass

def graph_album_release_vs_rank():
    """
    Graph album release date and rank for each song.
    """
    pass

def graph_top_artists_by_song_count():
    """
    Graph how many songs each artist has in the Top 100.
    """
    pass

def graph_artist_popularity_sum():
    """
    Make a pie chart of artists by the sum of the popularity of their top songs.
    """
    pass

# make all visuals
if __name__ == "__main__":
    cur, conn = connect_to_music_data("music_data.sqlite")
    graph_rank_vs_popularity(cur)
    graph_album_release_vs_rank(cur)
    graph_top_artists_by_song_count(cur)
    graph_artist_popularity_sum(cur)
    conn.close()
