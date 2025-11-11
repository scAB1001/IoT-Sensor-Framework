import azure.functions as func
import json
from datetime import datetime, timezone
from sensor_data_function import generate_sensor_readings
from statistics_function import analyze_sensor_data

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
               command_text="SELECT sensor_id, temperature, wind_speed, relative_humidity, co2_level, timestamp FROM dbo.sensor_data ORDER BY timestamp DESC",
               command_type="Text",
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

        analytics = analyze_sensor_data(sensor_list)

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

"""Performance Note:
# Test scalability with different loads
for count in 1 5 10 20 50; do
    time curl -s "https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api/simulate-data?sensor_count=$count" > /dev/null
    echo "Sensors: $count"
done

"""
