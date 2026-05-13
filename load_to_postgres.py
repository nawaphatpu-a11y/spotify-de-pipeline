import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging
from psycopg2.extras import execute_values
load_dotenv()

logging.basicConfig(
    level = logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("load_to_postgres.log"),
        logging.StreamHandler()
    ]
)

def connect():

    logging.info("Start Connected")
    conn = psycopg2.connect(
    f"host={os.getenv('RDS_HOST')} "
    f"port={os.getenv('RDS_PORT')} "
    f"dbname={os.getenv('RDS_NAME')} "
    f"user={os.getenv('RDS_USER')} "
    f"password={os.getenv('RDS_PASSWORD')}"
    )
    cur = conn.cursor()
    conn.commit()
    logging.info("Start Reading File")
    df = pd.read_csv("spotify_cleaned.csv", low_memory=False)
    engine = create_engine(
        f"postgresql://{os.getenv('RDS_USER')}:{os.getenv('RDS_PASSWORD')}@{os.getenv('RDS_HOST')}:{os.getenv('RDS_PORT')}/{os.getenv('RDS_NAME')}"
    )
    logging.info(f"Loaded {len(df)} rows")

    return conn, cur, df, engine

def load_dim(df, cur, conn):

    logging.info("Start loading Genres dimension")

    # load dim_genres
    genres = df[["track_genre"]].drop_duplicates().reset_index(drop = True)
    data = [(row["track_genre"],) for _, row in genres.iterrows()]
    execute_values(cur, "INSERT INTO dim_genres (track_genre) VALUES %s ON CONFLICT DO NOTHING", data)
    logging.info(f"Loaded {len(genres)} rows")
    logging.info("Start loading Artist dimension")

    # load dim_artists
    artist_name = df[["artists"]].drop_duplicates().reset_index(drop = True)
    data = [(row["artists"],) for _, row in artist_name.iterrows()]
    execute_values(cur,"INSERT INTO dim_artists (artist_name) VALUES %s ON CONFLICT DO NOTHING", data)
    logging.info(f"Loaded {len(artist_name)} rows")
    logging.info("Start loading Album dimension")

    # load dim_albums
    album_name = df[["album_name"]].drop_duplicates().reset_index(drop = True)
    data = [(row["album_name"],) for _, row in album_name.iterrows()]
    execute_values(cur, "INSERT INTO dim_albums (album_name) VALUES %s ON CONFLICT DO NOTHING", data)
    logging.info(f"Loaded {len(album_name)} rows")
    logging.info("Start loading Track dimension")

    # dim_tracks
    tracks = df[["track_id", "track_name", "explicit"]].drop_duplicates().reset_index(drop = True)
    data = [(row["track_id"], row["track_name"], row["explicit"]) for _, row in tracks.iterrows()]
    execute_values(cur, "INSERT INTO dim_tracks (track_id, track_name, explicit) VALUES %s ON CONFLICT DO NOTHING", data)
    logging.info(f"Loaded {len(tracks)} rows")
    logging.info("All Dimension loaded")
    conn.commit()
    return genres, artist_name, album_name, tracks

def merge_ids(engine, df):

    logging.info("Start merging ID")
    dim_artists_df = pd.read_sql("SELECT * FROM dim_artists", engine)
    dim_albums_df = pd.read_sql("SELECT * FROM dim_albums", engine)
    dim_genres_df = pd.read_sql("SELECT * FROM dim_genres", engine)

    artist_map = dim_artists_df.set_index("artist_name")["artist_id"].to_dict()
    album_map = dim_albums_df.set_index("album_name")["album_id"].to_dict()
    genre_map = dim_genres_df.set_index("track_genre")["genre_id"].to_dict()

    df["artist_id"] = df["artists"].map(artist_map)
    df["album_id"] = df["album_name"].map(album_map)
    df["genre_id"] = df["track_genre"].map(genre_map)
    logging.info("Finish loading")
    return df

def load_fact(df, cur, conn):
    logging.info("Start loading Fact")

    df_fact = df[[
        "track_id", "artist_id", "album_id", "genre_id",
        "popularity", "duration_ms", "danceability", "energy",
        "key", "loudness", "mode", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence", "tempo", "time_signature"
    ]].copy()
    
    df_fact["artist_id"] = df_fact["artist_id"].fillna(0).astype(int)
    df_fact["album_id"] = df_fact["album_id"].fillna(0).astype(int)
    
    chunksize = 5000
    total = len(df_fact)

    for start in range(0, total, chunksize):
        chunk = df_fact.iloc[start:start + chunksize]
        data = [tuple(row) for row in chunk.itertuples(index = False)]
        execute_values(cur,""" INSERT INTO fact_tracks( 
                track_id, artist_id, album_id, genre_id,
                popularity, duration_ms, danceability, energy,
                key, loudness, mode, speechiness, acousticness,
                instrumentalness, liveness, valence, tempo, time_signature
            ) VAlUES %s ON CONFLICT DO NOTHING """ , data)
        logging.info(f"Loading {min(start + chunksize, total)} / {total} rows into fact_tracks")
        conn.commit()
    logging.info("Finish loading")



def main():
    conn, cur, df , engine = connect()
    load_dim(df, cur ,conn)
    df = merge_ids(engine, df)
    load_fact(df, cur, conn)
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
