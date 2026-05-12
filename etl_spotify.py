import pandas as pd
import logging 
import os
import boto3
import io
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

def read_from_s3(key):
    logging.info("Start read from s3")
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    obj = s3.get_object(Bucket=os.getenv('AWS_BUCKET_NAME'), Key=key)
    logging.info("Data Ready!")
    return pd.read_csv(io.BytesIO(obj['Body'].read()))

def extract():
    logging.info("Extract started")

    df = read_from_s3('dataset.csv')
    logging.info(f"Loaded {len(df)} rows")
    return df

def validate():

    df = read_from_s3('dataset.csv')
    expected_type = {
        "popularity": "int64",
        "danceability" : "float64",
        "energy": "float64",
        "tempo": "float64"
    }

    for column, expected in expected_type.items():
        actual = str(df[column].dtype)
        if actual != expected:
            logging.warning(f"{column}: expected {expected} but got {actual}")
        else:
            logging.info(f"{column}: Ok ({actual})")
    

#print(df.shape)
#print(df.head())
#print(df.dtypes)
#print(df.isnull().sum())
#print(df.describe())

def transform():

    logging.info("Transform started")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = read_from_s3('dataset.csv')
    #df_genre_info = pd.DataFrame({
    #    "track_genre": ["pop","jazz","hip-hop","acoustic", "black-metal"],
    #    "mood": ["Happy", "Relaxed", "Energetic", "Calm", "Dark"]
    #})

    null_rows = df[df.isnull().any(axis=1)]
    null_rows.to_csv(os.path.join(base_dir, "Archived_null.csv"), index = False)
    
    df_clean = df.dropna()
    df_clean = df_clean.drop(columns=["Unnamed: 0"], errors = "ignore")

    #logging.info("Merge started")
    #df_clean = df_clean.merge(df_genre_info, on="track_genre", how = "left")
    #null_merge = df_clean["mood"].isnull().sum()
    
    print(f"Duplicate rows: {df_clean.duplicated().sum()}")
    print(df_clean[df_clean.duplicated(keep=False)].head())

    #logging.info(f"Merge complete: {null_merge} rows has no mood data")
    logging.info(f"Archived {len(null_rows)} null rows")
    logging.info(f"Clear data: {len(df_clean)} rows")

    df_clean.to_csv(os.path.join(base_dir, "spotify_cleaned.csv"), index=False) 
    return df_clean 

def load():
    logging.info("Load started")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_dir, "spotify_cleanded.csv"))
    df.to_csv(os.path.join(base_dir, "spotify_cleaned.csv"), index = False)
    logging.info("Load complete")

def main():
    extract()
    validate()
    transform()
    load()

if __name__ == "__main__":
    main()