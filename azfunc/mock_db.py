# mock_db.py

# Task 1 (must have 1 function and store in db)

class MockDatabase:
    def __init__(self):
        self.sensor_data = []
        self.analytics_data = []
        print("Mock database initialized - ready for storage operations")

    def store_sensor_data(self, sensor_readings, timestamp):
        """Mock storing sensor data"""
        if not sensor_readings:
            return False

        for sensor in sensor_readings:
            record = {
                'sensor_id': sensor['sensor_id'],
                'temperature': sensor['temperature'],
                'wind_speed': sensor['wind_speed'],
                'relative_humidity': sensor['relative_humidity'],
                'co2': sensor['co2'],
                'timestamp': timestamp
            }
            self.sensor_data.append(record)

        print(
            f"SUCCESS - Mock DB: Stored {len(sensor_readings)} sensor records")
        return True

    def store_analytics(self, analytics, timestamp, sensor_count):
        """Mock storing analytics data"""
        if not analytics:
            return False

        record = {
            'timestamp': timestamp,
            'sensor_count': sensor_count,
            'temperature_min': analytics['overall']['temperature']['min'],
            'temperature_max': analytics['overall']['temperature']['max'],
            'temperature_avg': analytics['overall']['temperature']['average'],
            'wind_min': analytics['overall']['wind_speed']['min'],
            'wind_max': analytics['overall']['wind_speed']['max'],
            'wind_avg': analytics['overall']['wind_speed']['average'],
            'humidity_min': analytics['overall']['relative_humidity']['min'],
            'humidity_max': analytics['overall']['relative_humidity']['max'],
            'humidity_avg': analytics['overall']['relative_humidity']['average'],
            'co2_min': analytics['overall']['co2']['min'],
            'co2_max': analytics['overall']['co2']['max'],
            'co2_avg': analytics['overall']['co2']['average']
        }
        self.analytics_data.append(record)

        print(f"SUCCESS - Mock DB: Stored analytics for {sensor_count} sensors")
        return True


# Global instance
mock_db = MockDatabase()
