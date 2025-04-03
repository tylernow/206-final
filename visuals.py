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
    conn = sqlite3.connect(path + "/" + "music_data.sqlite")
    cur = conn.cursor()
    return cur, conn

def graph_scatter_rank_vs_popularity(cur):
    """
    Graphs scatter plot on Billboard rank vs Spotify popularity.

    Parameters - database cursor

    Returns - nothing
    """
    ### retrieve ranks and popularities
    rank = []
    popularity = []
    # get data
    cur.execute(
        """
        SELECT rank, popularity
        FROM Songs
        WHERE popularity IS NOT NULL
        """
    )
    # process results
    result = cur.fetchall()
    for row in result:
        r = row[0]
        p = row[1]

        rank.append(r)
        popularity.append(p)
    
    ### make plot
    # create the graph
    fig, ax = plt.subplots()
    ax.plot(rank, rank, color='brown', label="Billboard Rank")
    ax.scatter(rank, popularity, marker='*', s=55, facecolors='gold', edgecolors='black', linewidths=0.3, label="Spotify Popularity")
    
    # start at origin
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    # label everything
    ax.set_xlabel('Ranking')
    ax.set_ylabel('Value')
    ax.set_title('Billboard Rank vs Spotify Popularity for Top 100 Songs')
    ax.legend()
    ax.grid()

    # save the graph
    fig.savefig("rank_vs_popularity.png")

    # show the graph
    plt.show()

def graph_scatter_album_release_vs_rank(cur):
    """
    Graph scatter plot of album release date vs rank for each song.

    Parameters - database cursor

    Returns - nothing
    """
    pass

def graph__bar_top_artists_by_song_count(cur):
    """
    Graph bar graph of number of top songs each artist has.

    Parameters - database cursor

    Returns - nothing
    """
    pass

def graph_pie_artist_popularity_sum(cur):
    """
    Make a pie chart of artists by the sum of the popularity of their top songs.

    Parameters - database cursor

    Returns - nothing
    """
    pass

# make all visuals
if __name__ == "__main__":
    cur, conn = connect_to_music_data()
    graph_scatter_rank_vs_popularity(cur)
    graph_scatter_album_release_vs_rank(cur)
    graph__bar_top_artists_by_song_count(cur)
    graph_pie_artist_popularity_sum(cur)
    conn.close()
