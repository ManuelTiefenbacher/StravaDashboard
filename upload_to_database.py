import json
import psycopg2
import os

# Connect to DB
conn = psycopg2.connect(
    host='manueltiefenbacher998.grafana.net',
    dbname='grafana-postgresql-datasource',
    port='5432',
    user='grafana_user',
    password='superSecretPassword123!'
)
cur = conn.cursor()

# Create table (run once)
cur.execute("""
    CREATE TABLE IF NOT EXISTS strava_activities (
        id BIGINT PRIMARY KEY,
        name TEXT,
        type TEXT,
        distance FLOAT,
        moving_time INTEGER,
        start_date TIMESTAMP
    );
""")

# Load data
with open("activities.json") as f:
    activities = json.load(f)

for a in activities:
    cur.execute("""
        INSERT INTO strava_activities (id, name, type, distance, moving_time, start_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (
        a['id'], a['name'], a['type'], a['distance'], a['moving_time'], a['start_date']
    ))

conn.commit()
cur.close()
conn.close()
print("Uploaded activities to DB.")