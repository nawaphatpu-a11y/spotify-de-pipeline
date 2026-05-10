from etl_spotify import extract, transform
import pandas as pd

def test_extract_row_count():
    df = extract()
    assert len(df) == 114000

def test_extract_columns():

    df = extract()
    expected_columns = ["track_id", "artists", "track_name","popularity", "track_genre"]
    for col in expected_columns:
        assert col in df.columns

def test_extract_dtypes():
    df = extract()
    assert df["popularity"].dtype == "int64"
    assert df["danceability"].dtype == "float64"
    assert df["energy"].dtype == "float64"
    assert df["tempo"].dtype == "float64"
    assert df["duration_ms"].dtype == "int64"
    assert df["key"].dtype == "int64"
    assert df["loudness"].dtype == "float64"
    assert df["mode"].dtype == "int64"
    assert df["speechiness"].dtype == "float64"
    assert df["acousticness"].dtype == "float64"
    assert df["instrumentalness"].dtype == "float64"
    assert df["liveness"].dtype == "float64"
    assert df["valence"].dtype == "float64"
    assert df["time_signature"].dtype == "int64"

def test_transform_no_null():
    df = transform()
    important_cols = ["track_id", "artists", "track_name","popularity", "track_genre"]
    assert df[important_cols].isnull().sum().sum() == 0

def test_transform_archived_nulls():
    transform()
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, "Archived_null.csv")
    assert os.path.exists(filepath)

    df_achived = pd.read_csv(filepath)
    assert len(df_achived) > 0


