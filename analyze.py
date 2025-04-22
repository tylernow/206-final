"""
analyze.py

This module performs analysis on the normalized SQLite database (music_data.sqlite)
created from Billboard and Spotify data.

It uses pandas to:
- Query and transform SQL data for analysis
- Export a summary text file
- Provide clean DataFrames for plotting and reporting
"""
import sqlite3
import pandas as pd

DB_NAME = "music_data.sqlite"

def get_rank_vs_popularity():
    """
    Retrieves each song's Billboard rank and Spotify popularity.

    Returns:
        pd.DataFrame: Contains two columns - 'rank' and 'popularity'

    """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""
        SELECT rank, popularity
        FROM Songs
        WHERE popularity IS NOT NULL
    """, conn)
    conn.close()
    return df

def get_album_release_vs_rank():
    """
    Retrieves album release dates and ranks for all songs.

    Returns:
        pd.DataFrame: Contains two columns - 'rank' and 'release_date'
    """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""
        SELECT Songs.rank, Albums.release_date
        FROM Songs
        JOIN Albums ON Songs.album_id = Albums.id
        WHERE Albums.release_date IS NOT NULL
    """, conn)
    conn.close()
    return df

def get_top_artists_by_song_count():
    """
    Counts how many Top 100 songs each artist has.

    Returns:
        pd.DataFrame: Contains 'artist' and 'song_count'
    """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""
        SELECT Artists.name AS artist, COUNT(*) AS song_count
        FROM Songs
        JOIN ArtistTopTracks ON Songs.name = ArtistTopTracks.track_name
        JOIN Artists ON ArtistTopTracks.artist_id = Artists.id
        GROUP BY Artists.name
        ORDER BY song_count DESC
    """, conn)
    conn.close()
    return df

def get_artist_popularity_sum():
    """
    Sums Spotify popularity scores for all songs by each artist.

    Returns:
        pd.DataFrame: Contains 'artist' and 'total_popularity'
    """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""
        SELECT Artists.name AS artist, SUM(Songs.popularity) AS total_popularity
        FROM Songs
        JOIN ArtistTopTracks ON Songs.name = ArtistTopTracks.track_name
        JOIN Artists ON ArtistTopTracks.artist_id = Artists.id
        GROUP BY Artists.name
        ORDER BY total_popularity DESC
    """, conn)
    conn.close()
    return df

def export_summary_text():
    """
    Writes a summary of the top 10 artists by song count and popularity to a text file.

    Output:
        analysis_summary.txt - Text file containing readable tables
    """
    top_artists = get_top_artists_by_song_count().head(10)
    popular_artists = get_artist_popularity_sum().head(10)

    with open("analysis_summary.txt", "w") as f:
        f.write("Top 10 Artists by # of Top 100 Songs:\n")
        f.write(top_artists.to_string(index=False))
        f.write("\n\nTop 10 Artists by Total Popularity:\n")
        f.write(popular_artists.to_string(index=False))
    print("✅ Summary written to analysis_summary.txt")

# Run this only when executing directly
if __name__ == "__main__":
    export_summary_text()
