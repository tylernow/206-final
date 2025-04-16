import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def connect_to_music_data():
    """
    Sets up a SQLite database connection and cursor to music_data.

    INPUT - NONE

    RETURNS - Tuple (cursor, connection)

    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "music_data.sqlite")
    cur = conn.cursor()
    return cur, conn

def graph_scatter_rank_vs_popularity(cur):
    """
    Graphs scatter plot on Billboard rank vs Spotify popularity.

    INPUT - database cursor
    OUTPUT - scatter plot of rank vs popularity
    RETURN - None
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
    ax.scatter(rank, popularity, marker='*', s=50, facecolors='gold', edgecolors='black', linewidths=0.3, label="Spotify Popularity")
    
    # start at origin
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    # label everything
    ax.set_xlabel('Billboard Ranking')
    ax.set_ylabel('Spotify Popularity')
    ax.set_title('Billboard Rank vs Spotify Popularity for Top 100 Songs')
    ax.grid()

    # save the graph
    fig.savefig("rank_vs_popularity.png", bbox_inches='tight')

    # show the graph
    plt.show()

def graph_scatter_album_release_rank_num(cur):
    """
    Graphs scatter plot of number of billboard ranking songs per album release date by year.

    INPUT - database cursor
    OUTPUT - scatter plot of number of ranking songs per release date by year
    RETURN - None
    """
    # get data
    releaseDate = []
    cur.execute(
        """
        SELECT Albums.release_date
        FROM Songs
        JOIN Albums ON Albums.id = Songs.album_id
        WHERE Albums.release_date IS NOT NULL
        ORDER BY Albums.release_date
        """
    )
    result = cur.fetchall()
    # process results
    for row in result:
        d = row[0][:7]
        y = d[0:4]

        releaseDate.append(d)
    
    # split release dates
    years = {}
    monthMarks = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    prevMonth = 0
    prevYear = ''
    for date in range(len(releaseDate)):
        y = releaseDate[date][:4]
        m = releaseDate[date][-2:]
        
        if y != prevYear:
            prevYear = y
            years[prevYear] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            
            prevMonth = 0
            for i in range(len(monthMarks)):
                if monthMarks[prevMonth] == m:
                    break
                prevMonth += 1
            years[prevYear][prevMonth] += 1
            continue
        
        while m != monthMarks[prevMonth]:
            prevMonth += 1
        
        years[prevYear][prevMonth] += 1
    

    ### make plot
    # create the graph
    fig, ax = plt.subplots()

    colors = ['darkblue', 'lightblue', 'turquoise', 'pink', 'lightgray']
    c = -1
    for year, months in years.items():
        c += 1
        ax.scatter(monthMarks, months, s=65, facecolors=colors[c], edgecolors='indigo', linewidths=0.5, label=year)
    
    # start at origin
    ax.set_ylim(bottom=0)
    # label everything
    ax.set_xlabel('Release Date (MM)')
    ax.set_ylabel('Number of Billboard Ranking Songs')
    ax.legend()
    ax.set_title(f"Number of Billboard Ranking Songs per Album Release Date as of {prevYear}-{monthMarks[prevMonth]} (YYYY-MM)")
    ax.grid()

    # save the graph
    fig.savefig("rank_by_album_release.png", bbox_inches='tight')

    # show the graph
    plt.show()    

def graph__bar_top_artists_by_song_count(cur):
    """
    Graph bar graph of number of top songs each artist has.

    INPUT - database cursor
    OUTPUT - bar graph of number of top songs per artist
    RETURN - None
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
    ax.set_title('Top Artists by Number of Ranking Songs')
    ax.grid()

    # save the graph
    fig.savefig("top_artists_by_song.png", bbox_inches='tight')

    # show the graph
    plt.show()    


def graph_pie_artist_popularity_sum(cur):
    """
    Makes a pie chart of artists by the sum of the popularity of their top songs.
    Special focus on the top 10 artists.

    INPUT - database cursor
    OUTPUT - pie chart of artists by sum of ranking song popularities
    RETURN - None
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
    # process results -- save top 10 artists
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
    colors = ['pink', 'purple', 'lightgray', 'lightgreen', 'ivory', 'slateblue', 'thistle', 'darkgreen', 'lightcyan', 'plum', 'cadetblue']
    explode = (0.18, 0.16, 0.14, 0.12, 0.1, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03)
    ax.set_title('Percent of Artists with Ranking Songs')

    plt.pie(popularity, explode=explode, labels=artist, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=100)
 
    # label everything
    plt.axis('equal')

    # save the graph
    fig.savefig("artists_by_popularity.png", bbox_inches='tight')

    # show the graph
    plt.show()    

# make all visuals
if __name__ == "__main__":
    cur, conn = connect_to_music_data()
    graph_scatter_rank_vs_popularity(cur)
    graph_scatter_album_release_rank_num(cur)
    graph__bar_top_artists_by_song_count(cur)
    graph_pie_artist_popularity_sum(cur)
    conn.close()
