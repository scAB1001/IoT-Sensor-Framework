import random

# Default the number of sensors to 20 for Task 1 if not specified
def generate_sensor_readings(sensor_count=20) -> list[dict]:
    """
    Generate simulated sensor data for Leeds with realistic random variations.
    Matches the exact requirements from Task 1.
    """
    sensors = []

    for sensor_id in range(1, sensor_count + 1):
        sensor_reading = {
            "sensor_id": sensor_id,
            "temperature": round(random.uniform(5, 18), 1),      # 5-18°C range
            "wind_speed": round(random.uniform(12, 24), 1),      # 12-24 mph range
            "relative_humidity": random.randint(30, 60),         # 30-60% range
            "co2_level": random.randint(400, 1600)               # 400-1600 ppm range
        }
        sensors.append(sensor_reading)

    return sensors