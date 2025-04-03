import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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
    Graphs scatter plot of album release date vs rank for each song.

    Parameters - database cursor

    Returns - nothing
    """
    # get data
    releaseDate = []
    rank = []
    cur.execute(
        """
        SELECT Albums.release_date, Songs.rank
        FROM Songs
        JOIN Albums ON Albums.id = Songs.album_id
        WHERE Albums.release_date IS NOT NULL
        ORDER BY Albums.release_date
        """
    )
    result = cur.fetchall()
    # process results
    for row in result:
        d = row[0]
        r = row[1]

        releaseDate.append(d)
        rank.append(r)

    ### make plot
    # create the graph
    fig, ax = plt.subplots()
    ax.scatter(releaseDate, rank, marker='^', s=55, facecolors='plum', edgecolors='indigo', linewidths=0.3)
    
    # start at origin
    ax.set_ylim(bottom=0)
    ax.set_xticks([min(releaseDate), (releaseDate[len(releaseDate) // 3]), max(releaseDate)])
    # label everything
    ax.set_xlabel('Release Date')
    ax.set_ylabel('Billboard Rank')
    ax.set_title('Album Release Date vs Billboard Rank for Top 100 Songs')
    ax.grid()

    # save the graph
    fig.savefig("albumRelease_vs_rank.png")

    # show the graph
    plt.show()    

def graph__bar_top_artists_by_song_count(cur):
    """
    Graph bar graph of number of top songs each artist has.

    Parameters - database cursor

    Returns - nothing
    """
    # get data
    artist = []
    count = []
    cur.execute(
        """
        SELECT Artists.name AS artist, COUNT(*) AS song_count
        FROM Songs
        JOIN ArtistTopTracks ON Songs.name = ArtistTopTracks.track_name
        JOIN Artists ON ArtistTopTracks.artist_id = Artists.id
        GROUP BY Artists.name
        ORDER BY song_count
        """
    )
    results = cur.fetchall()
    for row in results:
        a = row[0]
        c = row[1]

        artist.append(a)
        count.append(c)


    ### make plot
    # create the graph
    fig, ax = plt.subplots()

    width = 0.5
    colors = ['lightblue', 'mediumslateblue']
    ax.barh(artist, count, width, color=colors, edgecolor='black', hatch='/')

    # label everything
    ax.set_xlabel('Number of Top Songs')
    ax.set_ylabel('Artist')
    ax.set_title('Artists With Top Ranking Songs')
    ax.grid()

    # save the graph
    fig.savefig("top_artists_by_song.png")

    # show the graph
    plt.show()    


def graph_pie_artist_popularity_sum(cur):
    """
    Make a pie chart of artists by the sum of the popularity of their top songs.

    Parameters - database cursor

    Returns - nothing
    """
    popularity = []
    artist = []
    # collect data
    cur.execute(
        """
        SELECT Artists.name AS artist, SUM(Songs.popularity) AS total_popularity
        FROM Songs
        JOIN ArtistTopTracks ON Songs.name = ArtistTopTracks.track_name
        JOIN Artists ON ArtistTopTracks.artist_id = Artists.id
        GROUP BY Artists.name
        ORDER BY total_popularity DESC
        """
    )
    # process results
    result = cur.fetchall()
    remaining = 0
    count = 0
    for row in result:
        if(count < 10):
            a = row[0]
            p = row[1]

            artist.append(a)
            popularity.append(p)
            count += 1
        else:
            remaining += row[1]
    artist.append("Other")
    popularity.append(remaining)

    ### make plot
    # create the graph
    fig, ax = plt.subplots()
    colors = ['purple', 'forestgreen', 'slateblue', 'ivory', 'green', 'pink', 'gray', 'lightcyan', 'plum', 'blue', 'lightgray']
    explode = (0.15, 0.1, 0.075, 0.05, 0.01, 0, 0, 0, 0, 0, 0)

    plt.pie(popularity, explode=explode, labels=artist, colors=colors,
        autopct='%3.1f%%', shadow=True, startangle=100)
 
    # label everything
    plt.axis('equal')

    # save the graph
    fig.savefig("artists_by_popularity.png")

    # show the graph
    plt.show()    

# make all visuals
if __name__ == "__main__":
    cur, conn = connect_to_music_data()
    # graph_scatter_rank_vs_popularity(cur)
    # graph_scatter_album_release_vs_rank(cur) ## TODO -- complete labeling
    # graph__bar_top_artists_by_song_count(cur)
    # graph_pie_artist_popularity_sum(cur)
    conn.close()
