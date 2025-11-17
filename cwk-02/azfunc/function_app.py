import azure.functions as func
import json, logging
from datetime import datetime, timezone
from sensor_data_function import generate_sensor_readings
from statistics_function import analyze_data_per_sensor


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Task 1: Simulate Data Function
@app.function_name(name="SimulateDataFunction")
@app.route(route="simulate-data", methods=["GET"])
@app.sql_output(arg_name="sensorRecords",
                command_text="dbo.sensor_data",
                connection_string_setting="SqlConnectionString")
def simulate_data_function(req, sensorRecords):
    try:
        sensor_count = int(req.params.get('sensor_count', 20))
        sensor_data = generate_sensor_readings(sensor_count)
        timestamp = datetime.now(timezone.utc).isoformat()

        # Convert to SQL rows
        rows = []
        for sensor in sensor_data:
            row = func.SqlRow.from_dict({
                "sensor_id": sensor['sensor_id'],
                "temperature": sensor['temperature'],
                "wind_speed": sensor['wind_speed'],
                "relative_humidity": sensor['relative_humidity'],
                "co2_level": sensor['co2_level'],
                "timestamp": timestamp
            })
            rows.append(row)

        # Store in database via binding
        sensorRecords.set(rows)

        response_data = {
            "timestamp": timestamp,
            "sensor_count": sensor_count,
            "sensors": sensor_data,
            "database_status": f"Stored {len(sensor_data)} records"
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        error_response = json.dumps({"error": f"Simulation failed: {str(e)}"})
        return func.HttpResponse(error_response, mimetype="application/json", status_code=500)

# Task 2: Statistics Function
@app.function_name(name="StatisticsFunction")
@app.route(route="statistics", methods=["GET"])
@app.sql_input(arg_name="sensorData",
               command_text="SELECT sensor_id, temperature, wind_speed, relative_humidity, co2_level FROM dbo.sensor_data ORDER BY timestamp DESC",
               connection_string_setting="SqlConnectionString")
def statistics_function(req, sensorData):
    try:
        sensor_list = []

        for row in sensorData:
            sensor_list.append({
                'sensor_id': row['sensor_id'],
                'temperature': float(row['temperature']),
                'wind_speed': float(row['wind_speed']),
                'relative_humidity': row['relative_humidity'],
                'co2_level': row['co2_level']
            })

        if not sensor_list:
            return func.HttpResponse(
                json.dumps({"message": "No sensor data found"}),
                mimetype="application/json",
                status_code=200
            )

        # Get analytics with per-sensor statistics
        analytics = analyze_data_per_sensor(sensor_list)

        response_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data_analyzed": len(sensor_list),
            "analytics": analytics
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        error_response = json.dumps({"error": f"Statistics failed: {str(e)}"})
        return func.HttpResponse(error_response, mimetype="application/json", status_code=500)


# ========== TASK 3(a): Scheduled Data Collection ==========
# THIS RUNS EVERY 10 MINUTES, COMMENTED AND REDEPLOYED.
@app.function_name(name="ScheduledDataCollection")
@app.schedule(schedule="0 */10 * * * *", arg_name="timer", run_on_startup=True)
@app.sql_output(arg_name="sensorRecords",
                command_text="dbo.sensor_data",
                connection_string_setting="SqlConnectionString")
def scheduled_data_collection(timer, sensorRecords):
    """
    Timer-triggered function that automatically collects data from all 20 sensors every 10 minutes
    This satisfies Task 3(a): data collection at regular interval T
    """
    try:
        logging.info("🕒 Scheduled data collection triggered at %s",
                     datetime.now(timezone.utc).isoformat())

        sensor_count = 20  # All 20 sensors as required
        sensor_data = generate_sensor_readings(sensor_count)
        timestamp = datetime.now(timezone.utc).isoformat()

        # Convert to SQL rows
        rows = []
        for sensor in sensor_data:
            row = func.SqlRow.from_dict({
                "sensor_id": sensor['sensor_id'],
                "temperature": sensor['temperature'],
                "wind_speed": sensor['wind_speed'],
                "relative_humidity": sensor['relative_humidity'],
                "co2_level": sensor['co2_level'],
                "timestamp": timestamp
            })
            rows.append(row)

        # Store in database via binding
        sensorRecords.set(rows)

        logging.info(
            "✅ Scheduled collection: Stored data for %d sensors at %s", sensor_count, timestamp)

        # Log sample data for verification
        sample_sensor = sensor_data[0] if sensor_data else {}
        logging.info("📊 Sample sensor data: Sensor %d - Temp: %.1f°C, Wind: %.1f mph, Humidity: %d%%, CO2: %d ppm",
                     sample_sensor.get('sensor_id', 0),
                     sample_sensor.get('temperature', 0),
                     sample_sensor.get('wind_speed', 0),
                     sample_sensor.get('relative_humidity', 0),
                     sample_sensor.get('co2_level', 0))

    except Exception as e:
        logging.error("❌ Scheduled data collection failed: %s", str(e))


# ========== TASK 3(b): SQL Trigger for Automatic Statistics ==========
@app.function_name(name="SensorDataChangeTrigger")
@app.sql_trigger(arg_name="changes",
                 table_name="sensor_data",
                 connection_string_setting="SqlConnectionString")
@app.sql_input(arg_name="recentSensorData",
               command_text="""
              SELECT sensor_id, temperature, wind_speed, relative_humidity, co2_level, timestamp
              FROM dbo.sensor_data
              WHERE timestamp >= DATEADD(minute, -5, GETUTCDATE())
              ORDER BY timestamp DESC
              """,
               connection_string_setting="SqlConnectionString")
def sensor_data_change_trigger(changes, recentSensorData):
    """
    SQL Trigger that automatically runs when new data is inserted into sensor_data table
    This satisfies Task 3(b): automatic trigger when new data is stored
    And Task 3(c): outputs same statistics as Task 2
    """
    try:
        change_count = len(changes.get_changes()) if changes else 0
        logging.info("🚀 SQL Trigger activated! Detected %d changes in sensor_data table at %s",
                     change_count, datetime.now(timezone.utc).isoformat())

        # Convert SQL rows to Python list for analysis
        sensor_readings = []
        for row in recentSensorData:
            sensor_readings.append({
                'sensor_id': row['sensor_id'],
                'temperature': float(row['temperature']),
                'wind_speed': float(row['wind_speed']),
                'relative_humidity': row['relative_humidity'],
                'co2_level': row['co2_level'],
                'timestamp': str(row['timestamp'])
            })

        if not sensor_readings:
            logging.info("📭 No recent sensor data found for analysis")
            return

        # Calculate statistics using the same function as Task 2
        # This satisfies Task 3(c): same results as Task 2
        analytics = analyze_data_per_sensor(sensor_readings)

        # Log the statistics results
        logging.info("📈 AUTOMATIC STATISTICS CALCULATED:")
        logging.info("   Data analyzed: %d readings from %d sensors",
                     len(sensor_readings),
                     len(set(s['sensor_id'] for s in sensor_readings)))

        # Log detailed statistics
        temp_stats = analytics.get('temperature', {})
        wind_stats = analytics.get('wind_speed', {})
        humidity_stats = analytics.get('relative_humidity', {})
        co2_stats = analytics.get('co2_level', {})

        logging.info("   🌡️  Temperature: %.1f-%.1f°C (avg: %.1f°C)",
                     temp_stats.get('minimum', 0),
                     temp_stats.get('maximum', 0),
                     temp_stats.get('average', 0))

        logging.info("   💨 Wind Speed: %.1f-%.1f mph (avg: %.1f mph)",
                     wind_stats.get('minimum', 0),
                     wind_stats.get('maximum', 0),
                     wind_stats.get('average', 0))

        logging.info("   💧 Humidity: %d-%d%% (avg: %d%%)",
                     humidity_stats.get('minimum', 0),
                     humidity_stats.get('maximum', 0),
                     humidity_stats.get('average', 0))

        logging.info("   🏭 CO2 Levels: %d-%d ppm (avg: %d ppm)",
                     co2_stats.get('minimum', 0),
                     co2_stats.get('maximum', 0),
                     co2_stats.get('average', 0))

        # Check for environmental alerts
        check_environmental_alerts(analytics)

    except Exception as e:
        logging.error("❌ SQL Trigger execution failed: %s", str(e))


def check_environmental_alerts(analytics):
    """
    Check for environmental conditions that might require alerts
    Enhanced feature for realistic scenario
    """
    try:
        temp_stats = analytics.get('temperature', {})
        co2_stats = analytics.get('co2_level', {})
        humidity_stats = analytics.get('relative_humidity', {})

        # Heatwave alert
        if temp_stats.get('maximum', 0) > 25:
            logging.warning("🔥 HEATWAVE ALERT: High temperature detected (%.1f°C)",
                            temp_stats.get('maximum', 0))

        # High pollution alert
        if co2_stats.get('maximum', 0) > 1200:
            logging.warning("🏭 POLLUTION ALERT: High CO2 levels detected (%d ppm)",
                            co2_stats.get('maximum', 0))

        # High humidity alert
        if humidity_stats.get('maximum', 0) > 80:
            logging.warning("💧 HUMIDITY ALERT: High humidity levels detected (%d%%)",
                            humidity_stats.get('maximum', 0))

        # Very low temperature alert
        if temp_stats.get('minimum', 0) < 0:
            logging.warning("❄️ COLD ALERT: Freezing temperatures detected (%.1f°C)",
                            temp_stats.get('minimum', 0))

    except Exception as e:
        logging.error("Error in environmental alert checking: %s", str(e))
