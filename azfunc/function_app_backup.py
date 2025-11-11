import azure.functions as func
import json
from datetime import datetime, timezone
from sensor_data_function import generate_sensor_readings
from statistics_function import analyze_sensor_data

app = func.FunctionApp(
    http_auth_level=func.AuthLevel.ANONYMOUS)  # Was .FUNCTION

# Task 1: Simulate Data Function - FIXED ROUTE


@app.function_name(name="SimulateDataFunction")
@app.route(route="simulate-data", methods=["GET"])
@app.sql_output(arg_name="sensorRecords",
                command_text="dbo.sensor_data",
                connection_string_setting="SqlConnectionString")
def simulate_data_function(req: func.HttpRequest, sensorRecords: func.Out[func.SqlRow]) -> func.HttpResponse:
    """
    HTTP Trigger that generates sensor data and stores it in Azure SQL Database
    using SQL output binding.
    """
    try:
        # Get sensor count from query parameter instead of route
        sensor_count = int(req.params.get('sensor_count', 20))

        # Generate sensor data
        sensor_data = generate_sensor_readings(sensor_count)
        timestamp = datetime.now(
            timezone.utc).isoformat()

        # Convert to SQL rows for output binding
        rows = []
        for sensor in sensor_data:
            # Azure SQL binding expects specific column names matching your table
            row = func.SqlRow.from_dict({
                "sensor_id": sensor['sensor_id'],
                "temperature": sensor['temperature'],
                "wind_speed": sensor['wind_speed'],
                "relative_humidity": sensor['relative_humidity'],
                "co2_level": sensor['co2_level'],
                "timestamp": timestamp
            })
            rows.append(row)

        # This automatically inserts into SQL Database via binding
        sensorRecords.set(rows)

        # Return the generated data as JSON response
        response_data = {
            "timestamp": timestamp,
            "sensor_count": sensor_count,
            "sensors": sensor_data,
            "database_status": f"Stored {len(sensor_data)} records in Azure SQL Database"
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        error_response = json.dumps({"error": f"Simulation failed: {str(e)}"})
        return func.HttpResponse(error_response, mimetype="application/json", status_code=500)

# Task 2: Statistics Function - FIXED ROUTE


@app.function_name(name="StatisticsFunction")
@app.route(route="statistics", methods=["GET"])
@app.sql_input(arg_name="sensorData",
               command_text="SELECT TOP ({data_limit}) sensor_id, temperature, wind_speed, relative_humidity, co2_level, timestamp FROM dbo.sensor_data ORDER BY timestamp DESC",
               command_type="Text",
               parameters="data_limit={data_limit}",
               connection_string_setting="SqlConnectionString")
def statistics_function(req: func.HttpRequest, sensorData: func.SqlRowList) -> func.HttpResponse:
    """
    HTTP Trigger that reads sensor data from Azure SQL Database using SQL input binding
    and calculates statistics.
    """
    try:
        # Get data limit from query parameter instead of route
        data_limit = int(req.params.get('data_limit', 100)
                         )  # ← CHANGED to req.params

        # Convert SQL rows to Python list (sensorData is populated automatically by binding)
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
                json.dumps({"error": "No sensor data found in database"}),
                mimetype="application/json",
                status_code=404
            )

        # Generate statistics
        analytics = analyze_sensor_data(sensor_list)

        response_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data_analyzed": len(sensor_list),
            "data_source": "Azure SQL Database",
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

# Task 3a: Timer Trigger for Automatic Data Collection
# @app.function_name(name="ScheduledDataCollection")
# # Every 5 minutes
# @app.schedule(schedule="0 */5 * * * *", arg_name="timer", run_on_startup=False)
# @app.sql_output(arg_name="sensorRecords",
#                 command_text="dbo.sensor_data",
#                 connection_string_setting="SqlConnectionString")
# def scheduled_data_collection(timer: func.TimerRequest, sensorRecords: func.Out[func.SqlRow]) -> None:
#     """
#     Timer Trigger that automatically generates and stores sensor data every 5 minutes.
#     This satisfies Task 3a requirement.
#     """
#     try:
#         # Generate data for 20 sensors (Leeds requirement)
#         sensor_data = generate_sensor_readings(20)
#         timestamp = datetime.now(timezone.utc).isoformat()

#         # Convert to SQL rows
#         rows = []
#         for sensor in sensor_data:
#             row = func.SqlRow.from_dict({
#                 "sensor_id": sensor['sensor_id'],
#                 "temperature": sensor['temperature'],
#                 "wind_speed": sensor['wind_speed'],
#                 "relative_humidity": sensor['relative_humidity'],
#                 "co2_level": sensor['co2_level'],
#                 "timestamp": timestamp
#             })
#             rows.append(row)

#         # Store in database via output binding
#         sensorRecords.set(rows)

#         print(
#             f"✅ Timer Trigger: Stored {len(sensor_data)} sensor records at {timestamp}")

#     except Exception as e:
#         print(f"❌ Timer Trigger failed: {e}")
