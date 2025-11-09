import json
import random
import logging
from datetime import datetime, timezone
from typing import List, Dict, Union


def handle_sensor_request(req) -> str:
    logging.info(
        'Python HTTP trigger function processed a request for sensor data.')

    try:
        # Get number of sensors from route parameter (optional)
        sensor_count_param = req.route_params.get('sensor_count')

        if sensor_count_param:
            sensor_count = int(sensor_count_param)
        else:
            # Default to 20 if no parameter provided
            sensor_count = 20

        # Generate sensor data
        sensor_data = generate_sensor_readings(sensor_count)

        # Add timestamp
        response_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sensor_count": sensor_count,
            "sensors": sensor_data
        }

        return json.dumps(response_data, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


def generate_sensor_readings(sensor_count: int) -> List[Dict[str, Union[float, int]]]:
    sensors = []

    for sensor_id in range(1, sensor_count + 1):
        sensor_reading = {
            "sensor_id": sensor_id,
            "temperature": round(random.uniform(5, 18), 1), # Temperature in Degrees Celsius
            "wind_speed": round(random.uniform(12, 24), 1), # Wind speed in Miles per hour (mph)
            "relative_humidity": random.randint(30, 60), # Relative humidity in percentage (%)
            "co2_level": random.randint(400, 1600) # CO2 level in parts per million (ppm)
        }
        sensors.append(sensor_reading)

    return sensors
