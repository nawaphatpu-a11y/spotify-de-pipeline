FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY etl_spotify.py .
COPY load_to_postgres.py .
CMD [ "python", "etl_spotify.py" ]