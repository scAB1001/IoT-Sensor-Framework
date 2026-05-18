
def calculate_basic_stats(values: list) -> dict:
    """Calculate minimum, maximum, and average for a list of values"""
    if not values:
        return {"minimum": 0.0, "maximum": 0.0, "average": 0.0}

    return {
        "minimum": min(values),
        "maximum": max(values),
        "average": round(sum(values) / len(values), 2)
    }


def analyze_data_per_sensor(sensor_data: list) -> dict:
    """
    Analyze sensor data to calculate statistics per sensor id.
    Returns minimum, maximum, and average for each measurement type.
    """
    if not sensor_data:
        return {"error": "No sensor data provided"}

    # Group data by sensor_id
    sensor_groups = {}
    for sensor in sensor_data:
        sensor_id = sensor['sensor_id']
        if sensor_id not in sensor_groups:
            sensor_groups[sensor_id] = {
                'temperatures': [],
                'wind_speeds': [],
                'humidities': [],
                'co2_levels': []
            }

        sensor_groups[sensor_id]['temperatures'].append(sensor['temperature'])
        sensor_groups[sensor_id]['wind_speeds'].append(sensor['wind_speed'])
        sensor_groups[sensor_id]['humidities'].append(
            sensor['relative_humidity'])
        sensor_groups[sensor_id]['co2_levels'].append(sensor['co2_level'])

    # Calculate statistics for each sensor
    result = {}
    for sensor_id, data in sensor_groups.items():
        result[sensor_id] = {
            "temperature": calculate_basic_stats(data['temperatures']),
            "wind_speed": calculate_basic_stats(data['wind_speeds']),
            "relative_humidity": calculate_basic_stats(data['humidities']),
            "co2_level": calculate_basic_stats(data['co2_levels'])
        }

    return result
