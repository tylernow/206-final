import sqlite3
import pandas as pd

DB_NAME = "music_data.sqlite"

def get_rank_vs_popularity():
    """
    Get Billboard rank vs Spotify popularity.
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
    Get album release date and rank for each song.
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
    Count how many songs each artist has in the Top 100.
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
    Sum popularity of songs by each artist.
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
    Write summary stats to a text file.
    """
    top_artists = get_top_artists_by_song_count().head(10)
    popular_artists = get_artist_popularity_sum().head(10)

    with open("analysis_summary.txt", "w") as f:
        f.write("🎤 Top 10 Artists by # of Top 100 Songs:\n")
        f.write(top_artists.to_string(index=False))
        f.write("\n\n🔥 Top 10 Artists by Total Popularity:\n")
        f.write(popular_artists.to_string(index=False))
    print("✅ Summary written to analysis_summary.txt")

# Run this only when executing directly
if __name__ == "__main__":
    export_summary_text()
