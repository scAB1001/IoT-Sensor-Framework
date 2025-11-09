import azure.functions as func
import json
from hello_function import handle_hello_request
from sensor_data_function import handle_sensor_request
from statistics_function import handle_analytics_request

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Hello World Function
@app.function_name(name="HttpExample")
@app.route(route="hello")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    response_text = handle_hello_request(req)
    print("Response Text:", response_text)
    return func.HttpResponse(response_text, status_code=200)
    # return func.HttpResponse(status_code=200)

# Sensor Data Function - SINGLE ROUTE with optional parameter
@app.function_name(name="GenerateSensorData")
@app.route(route="sensors/{sensor_count?}", methods=["GET"])
def generate_sensor_data(req: func.HttpRequest) -> func.HttpResponse:
    response_text = handle_sensor_request(req)

    # Check if it's an error response
    if "error" in response_text:
        return func.HttpResponse(
            response_text,
            mimetype="application/json",
            status_code=500
        )
    else:
        return func.HttpResponse(
            response_text,
            mimetype="application/json",
            status_code=200
        )

# Statistics Function - Uses sensor data JSON from request body
# Analytics Function (Task 2) - Processes sensor data with statistics


@app.function_name(name="SensorAnalytics")
@app.route(route="analytics/{sensor_count?}", methods=["GET"])
def sensor_analytics(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # First, get sensor data
        sensor_count = req.route_params.get('sensor_count', 20)
        sensor_response = handle_sensor_request(
            req)  # Reuse the sensor function

        if "error" in sensor_response:
            return func.HttpResponse(sensor_response, mimetype="application/json", status_code=500)

        # Process analytics on the sensor data
        analytics_response = handle_analytics_request(sensor_response)

        return func.HttpResponse(
            analytics_response,
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        error_response = json.dumps({"error": f"Analytics failed: {str(e)}"})
        return func.HttpResponse(error_response, mimetype="application/json", status_code=500)
