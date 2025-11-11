import azure.functions as func
import json
import logging
from datetime import datetime, timezone

# Import your modular functions
from sensor_data_function import generate_sensor_readings
from statistics_function import analyze_sensor_data

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Test function


@app.function_name(name="TestFunction")
@app.route(route="test", methods=["GET"])
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({
            "message": "Test function working!",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }),
        mimetype="application/json",
        status_code=200
    )

# Task 1: Simulate Data Function using your module


@app.function_name(name="SimulateDataFunction")
@app.route(route="simulate-data", methods=["GET", "POST"])
@app.sql_output(arg_name="sensorRecords",
                command_text="dbo.sensor_data",
                connection_string_setting="SqlConnectionString")
def simulate_data_function(req: func.HttpRequest, sensorRecords: func.Out[func.SqlRow]) -> func.HttpResponse:
    try:
        # Get sensor count from request
        sensor_count = 20  # Default to 20 sensors as required
        if req.method == "GET":
            sensor_count = int(req.params.get('sensor_count', 20))
        elif req.method == "POST":
            try:
                req_body = req.get_json()
                sensor_count = int(req_body.get('sensor_count', 20))
            except ValueError:
                pass

        # Use your modular function to generate sensor data
        sensors_data = generate_sensor_readings(sensor_count)

        # Prepare SQL rows for output binding
        rows = []
        for sensor in sensors_data:
            sql_row = func.SqlRow.from_dict({
                "sensor_id": sensor["sensor_id"],
                "temperature": sensor["temperature"],
                "wind_speed": sensor["wind_speed"],
                "relative_humidity": sensor["relative_humidity"],
                "co2_level": sensor["co2_level"],
                "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            })
            rows.append(sql_row)

        # Store in database
        sensorRecords.set(rows)

        response_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sensor_count": sensor_count,
            "sensors": sensors_data,
            "database_status": f"Successfully stored {sensor_count} sensor records"
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error in simulate_data_function: {str(e)}")
        error_response = json.dumps({"error": f"Simulation failed: {str(e)}"})
        return func.HttpResponse(error_response, mimetype="application/json", status_code=500)

# Task 2: Statistics Function using your module


@app.function_name(name="StatisticsFunction")
@app.route(route="statistics", methods=["GET"])
@app.sql_input(arg_name="sensorData",
               command_text="""
              SELECT sensor_id, temperature, wind_speed, relative_humidity, co2_level, timestamp
              FROM dbo.sensor_data
              WHERE timestamp >= DATEADD(hour, -1, GETUTCDATE())
              ORDER BY timestamp DESC
              """,
               command_type="Text",
               connection_string_setting="SqlConnectionString")
def statistics_function(req: func.HttpRequest, sensorData: func.SqlRowList) -> func.HttpResponse:
    try:
        # Convert SQL rows to dictionary format for your analysis module
        sensor_readings = []
        for row in sensorData:
            sensor_readings.append({
                'sensor_id': row['sensor_id'],
                'temperature': float(row['temperature']),
                'wind_speed': float(row['wind_speed']),
                'relative_humidity': int(row['relative_humidity']),
                'co2_level': int(row['co2_level']),
                'timestamp': str(row['timestamp'])
            })

        if not sensor_readings:
            return func.HttpResponse(
                json.dumps({
                    "message": "No sensor data found in database for the last hour",
                    "data_analyzed": 0,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }),
                mimetype="application/json",
                status_code=200
            )

        # Use your modular function to calculate statistics
        stats_result = analyze_sensor_data(sensor_readings)

        response_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data_analyzed": len(sensor_readings),
            "sensors_analyzed": len(set([s['sensor_id'] for s in sensor_readings])),
            "time_period": "last hour",
            "statistics": stats_result
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error in statistics_function: {str(e)}")
        error_response = json.dumps(
            {"error": f"Statistics calculation failed: {str(e)}"})
        return func.HttpResponse(error_response, mimetype="application/json", status_code=500)


# COMMENTED OUT FOR NOW
# # Task 3(a): Timer-triggered automatic data collection
# @app.function_name(name="ScheduledDataCollection")
# @app.schedule(schedule="0 */10 * * * *", arg_name="timer", run_on_startup=False)
# @app.sql_output(arg_name="sensorRecords",
#                 command_text="dbo.sensor_data",
#                 connection_string_setting="SqlConnectionString")
# def scheduled_data_collection(timer: func.TimerRequest, sensorRecords: func.Out[func.SqlRow]) -> None:
#     """Automatically collect data from all 20 sensors every 10 minutes"""
#     logging.info("Scheduled data collection triggered")

#     try:
#         sensor_count = 20
#         # Use your modular function
#         sensors_data = generate_sensor_readings(sensor_count)

#         rows = []
#         for sensor in sensors_data:
#             sql_row = func.SqlRow.from_dict({
#                 "sensor_id": sensor["sensor_id"],
#                 "temperature": sensor["temperature"],
#                 "wind_speed": sensor["wind_speed"],
#                 "relative_humidity": sensor["relative_humidity"],
#                 "co2_level": sensor["co2_level"],
#                 "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
#             })
#             rows.append(sql_row)

#         sensorRecords.set(rows)
#         logging.info(
#             f"Successfully stored {sensor_count} sensor records via scheduled trigger")

#     except Exception as e:

#         logging.error(f"Error in scheduled data collection: {str(e)}")

# COMMENTED OUT FOR NOW
# # Task 3: Timer-triggered function for automatic data collection
# @app.function_name(name="ScheduledDataCollection")
# # Every 10 minutes
# @app.schedule(schedule="0 */10 * * * *", arg_name="timer", run_on_startup=False)
# @app.sql_output(arg_name="sensorRecords",
#                 command_text="dbo.sensor_data",
#                 connection_string_setting="SqlConnectionString")
# def scheduled_data_collection(timer: func.TimerRequest, sensorRecords: func.Out[func.SqlRow]) -> None:
#     """Automatically collect data from all 20 sensors every 10 minutes"""
#     logging.info("Scheduled data collection triggered")

#     try:
#         sensor_count = 20
#         rows = []

#         for sensor_id in range(1, sensor_count + 1):
#             sensor_data = {
#                 "sensor_id": sensor_id,
#                 "temperature": round(random.uniform(5, 18), 1),
#                 "wind_speed": round(random.uniform(12, 24), 1),
#                 "relative_humidity": random.randint(30, 60),
#                 "co2_level": random.randint(400, 1600),
#                 "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
#             }

#             row = func.SqlRow.from_dict(sensor_data)
#             rows.append(row)

#         sensorRecords.set(rows)
#         logging.info(
#             f"Successfully stored {sensor_count} sensor records via scheduled trigger")

#     except Exception as e:
#         logging.error(f"Error in scheduled data collection: {str(e)}")
