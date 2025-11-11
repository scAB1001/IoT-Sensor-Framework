from typing import Dict, List, Any


def calculate_basic_stats(values: List[float]) -> Dict[str, float]:
    """Calculate minimum, maximum, and average for a list of values"""
    if not values:
        return {"minimum": 0.0, "maximum": 0.0, "average": 0.0}

    return {
        "minimum": min(values),
        "maximum": max(values),
        "average": round(sum(values) / len(values), 2)
    }


def analyze_sensor_data(sensor_data: List[Dict]) -> Dict[str, Any]:
    """
    Analyze sensor data to calculate statistics.
    Returns minimum, maximum, and average for each measurement type.
    """
    if not sensor_data:
        return {"error": "No sensor data provided"}

    # Extract all readings
    temperatures = [sensor['temperature'] for sensor in sensor_data]
    wind_speeds = [sensor['wind_speed'] for sensor in sensor_data]
    humidity_levels = [sensor['relative_humidity'] for sensor in sensor_data]
    co2_levels = [sensor['co2_level'] for sensor in sensor_data]

    # Calculate statistics (Task 2)
    stats = {
        "temperature": calculate_basic_stats(temperatures),
        "wind_speed": calculate_basic_stats(wind_speeds),
        "relative_humidity": calculate_basic_stats(humidity_levels),
        "co2_level": calculate_basic_stats(co2_levels)
    }

    return stats
