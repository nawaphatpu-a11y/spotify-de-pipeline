import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    f"host={os.getenv('RDS_HOST')} "
    f"port={os.getenv('RDS_PORT')} "
    f"dbname={os.getenv('RDS_NAME')} "
    f"user={os.getenv('RDS_USER')} "
    f"password={os.getenv('RDS_PASSWORD')}"
)

cur = conn.cursor()

with open("init.sql", "r") as f:
    sql = f.read()

cur.execute(sql)
conn.commit()
print("Tables created successfully!")
cur.close()
conn.close()