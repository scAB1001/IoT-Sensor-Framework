import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'sensor_data.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-style access
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SensorData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        wind_speed REAL,
        relative_humidity INTEGER,
        co2_level INTEGER,
        created_at TEXT,
        updated_at TEXT
    )
    ''')

    conn.commit()
    conn.close()
