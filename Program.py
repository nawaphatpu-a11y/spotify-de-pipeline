import pandas as pd
import numpy as np

df = pd.read_csv("dataset.csv")
df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

df = df.drop(columns='Unnamed: 0')

#print(df.head())

#print(df.dtypes, end = "\n\n")

df_blank_archive = df[df.isnull().any(axis=1)]
df_completed = df.dropna()

df_clean = df.drop_duplicates(subset=["track_id"], keep="last")
df_duplicated = df[df.duplicated(subset=["track_id"], keep="last")]
#print(df_completed.shape[0])
#print(df.shape)
#print(df_clean.shape)
#print(df_clean.shape[0] + df_duplicated.shape[0])

#print(df_clean.dtypes)
print(df_clean["explicit"].unique())