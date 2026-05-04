import pandas as pd

df_track = pd.DataFrame({
    "track_name": ["Song A", "Song B", "Song C", "Song D"],
    "track_genre": ["pop", "jazz", "pop", "metal"]
})

df_genre = pd.DataFrame({
    "track_genre": ["pop", "jazz"],
    "mood": ["Happy", "Relaxed"]
})

df_left = df_track.merge(df_genre , on = "track_genre" , how = "left")
print(df_left)
print("---")

df_inner = df_track.merge(df_genre, on = "track_genre", how = "inner")
print(df_inner)