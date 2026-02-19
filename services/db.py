import sqlite3

DB_NAME = "sensor_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            co2 REAL,
            temperature REAL,
            humidity REAL,
            quality TEXT,
            score INTEGER,
            latitude REAL,
            longitude REAL,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_reading(reading):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO readings (
            name, co2, temperature, humidity, quality, score,
            latitude, longitude, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        reading["name"],
        reading["co2"],
        reading["temperature"],
        reading["humidity"],
        reading["quality"],
        reading["score"],
        reading["latitude"],
        reading["longitude"],
        reading["timestamp"]
    ))

    conn.commit()
    conn.close()


def get_latest_readings(limit=50):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT name, co2, temperature, humidity, quality, score,
               latitude, longitude, timestamp
        FROM readings
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return rows
