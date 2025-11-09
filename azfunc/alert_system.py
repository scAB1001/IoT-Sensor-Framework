from typing import List, Dict, Any


def generate_alerts(stats: Dict[str, Dict]) -> Dict[str, Any]:
    """Generate alert messages based on statistics"""
    alerts = []

    if stats["temperature"]["heatwave_alert"]:
        alerts.append("HEATWAVE ALERT: High temperatures detected")
    if stats["temperature"]["cold_wave_alert"]:
        alerts.append("COLD WAVE ALERT: Low temperatures detected")
    if stats["wind"]["high_wind_alert"]:
        alerts.append("HIGH WIND ALERT: Strong winds detected")
    if stats["co2"]["critical_pollution_alert"]:
        alerts.append("CRITICAL POLLUTION ALERT: Very high CO2 levels")
    elif stats["co2"]["pollution_alert"]:
        alerts.append("POLLUTION ALERT: High CO2 levels detected")
    if stats["humidity"]["high_humidity_alert"]:
        alerts.append("HIGH HUMIDITY ALERT: Very humid conditions")
    if stats["humidity"]["low_humidity_alert"]:
        alerts.append("LOW HUMIDITY ALERT: Dry conditions detected")

    return {
        "total_alerts": len(alerts),
        "alert_messages": alerts
    }
