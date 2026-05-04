import sqlite3
import pandas as pd

df = pd.read_csv("dataset.csv")

conn = sqlite3.connect("spotify.db")
df.to_sql("tracks", conn, if_exists="replace", index = False)
conn.close()

print("Done! spotify.db created")