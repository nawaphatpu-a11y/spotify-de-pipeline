import pandas as pd
df = pd.read_csv("spotify_cleaned.csv")

print(f"artist_id null: {df['artists'].nunique()}")
print(f"album_id null: {df['album_name'].nunique()}")
print(f"genre_id null: {df['track_genre'].nunique()}")
