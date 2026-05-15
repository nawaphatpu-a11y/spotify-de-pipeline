from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col
from pyspark.sql.types import IntegerType

spark = SparkSession.builder \
    .appName("SpotifyETL")\
    .getOrCreate()

df = spark.read.csv(r"C:\Users\User\Desktop\Project\dataset.csv", header=True ,inferSchema=True)
print(f"Row count: {df.count()}")

df = df.drop("_c0")
df = df.withColumn("popularity", col("popularity").cast(IntegerType()))
df = df.dropna(subset=["track_genre", "popularity"])
df = df.filter(col("track_genre").rlike("^[a-zA-Z]"))
df.groupBy("track_genre").agg(avg("popularity")).show()



spark.stop()