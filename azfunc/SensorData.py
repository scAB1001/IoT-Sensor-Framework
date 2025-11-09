import sqlite3
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from db import create_tables, get_connection
from typing import List


def init_db():
    create_tables()


class BaseModel(ABC):
    """
    Abstract base class for all models using raw SQLite.
    Provides basic save() and delete() methods.
    """

    created_at: str
    updated_at: str

    def __init__(self):
        now = datetime.now(timezone.utc).isoformat()
        self.created_at = now
        self.updated_at = now

    @abstractmethod
    def _insert_query(self) -> tuple[str, tuple]:
        """Returns a (SQL string, parameters) tuple for insertion"""
        pass

    # @abstractmethod
    # def _delete_query(self) -> tuple[str, tuple]:
    #     """Returns a (SQL string, parameters) tuple for deletion"""
    #     pass

    def save(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query, params = self._insert_query()
            cursor.execute(query, params)
            conn.commit()
            conn.close()
        except Exception as e:
            print("Save Error:", e)
            return e

    # def delete(self):
    #     try:
    #         conn = get_connection()
    #         cursor = conn.cursor()
    #         query, params = self._delete_query()
    #         cursor.execute(query, params)
    #         conn.commit()
    #         conn.close()
    #     except Exception as e:
    #         print("Delete Error:", e)
    #         return e


class SensorData(BaseModel):
    def __init__(self, temperature, wind_speed, relative_humidity, co2_level):
        super().__init__()
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.relative_humidity = relative_humidity
        self.co2_level = co2_level

    def _insert_query(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM sensor_data WHERE id = ?", (self,))
        if cursor.fetchone():
            raise ValueError(
                f"Sensor data already exists in database: <{self}>")

        conn.close()
        return (
            '''
            INSERT INTO SensorData (
                temperature, wind_speed, relative_humidity, co2_level,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                self.temperature, self.wind_speed, self.relative_humidity, self.co2_level,
                self.created_at, self.updated_at
            )
        )

    # def _delete_query(self):
    #     return ('DELETE FROM SensorData WHERE id = ?', (self,))

    @classmethod
    def get_all_sensors(cls):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM SensorData ORDER BY created_at")
        rows = cur.fetchall()
        conn.close()
        return rows

    # def _delete_query(self, id):
    #     return ('DELETE FROM SensorData WHERE id = ?', (selfid,))

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM SensorData WHERE id = ?", (id,))
        result = cur.fetchone()
        conn.close()
        return result

