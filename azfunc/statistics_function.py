from typing import Dict, List, Any
import json
import random
import logging
from datetime import datetime, timezone
from typing import List, Dict, Union


def calculate_basic_stats(values: List[float]) -> Dict[str, float]:
    """Calculate basic statistics for a list of values"""
    if not values:
        return {"average": 0.0, "max": 0.0, "min": 0.0}

    return {
        "min": min(values),
        "max": max(values),
        "average": round(sum(values) / len(values), 2)
    }


def analyze_sensor_data(sensor_data: List[Dict]) -> Dict[str, Any]:
    """
    Analyze sensor data to provide overall AND per-sensor statistics
    """
    if not sensor_data:
        return {"error": "No sensor data provided"}

    # Extract all readings for overall statistics
    temperatures = [sensor['temperature'] for sensor in sensor_data]
    wind_speeds = [sensor['wind_speed'] for sensor in sensor_data]
    relative_humidity_levels = [sensor['relative_humidity']
                                for sensor in sensor_data]
    co2_levels = [sensor['co2_level'] for sensor in sensor_data]

    # # Calculate per-sensor statistics
    # per_sensor_stats = []
    # for sensor in sensor_data:
    #     sensor_stats = {
    #         "sensor_id": sensor['sensor_id'],
    #         "temperature": sensor['temperature'],
    #         "wind_speed": sensor['wind_speed'],
    #         "relative_humidity": sensor['relative_humidity'],
    #         "co2": sensor['co2'],
    #     }
    #     per_sensor_stats.append(sensor_stats)

    # Calculate overall statistics
    overall_stats = {
        "temperature": calculate_basic_stats(temperatures),
        "wind_speed": calculate_basic_stats(wind_speeds),
        "relative_humidity": calculate_basic_stats(relative_humidity_levels),
        "co2_level": calculate_basic_stats(co2_levels)
    }

    # Combine both types of statistics
    stats = {
        "overall": overall_stats
    }

    return stats



def handle_analytics_request(sensor_data_json: str) -> str:
    """
    Process analytics request and return statistics
    """
    try:
        # Parse sensor data
        data = json.loads(sensor_data_json)
        sensors = data.get("sensors", [])

        # Perform analytics
        analytics = analyze_sensor_data(sensors)

        # Combine with original data
        response_data = {
            "timestamp": data.get("timestamp"),
            "sensor_count": data.get("sensor_count"),
            "sensors": sensors,
            "analytics": analytics
        }

        return json.dumps(response_data, indent=2)

    except Exception as e:
        logging.error(f"Analytics error: {str(e)}")
        return json.dumps({"error": f"Analytics processing failed: {str(e)}"})
