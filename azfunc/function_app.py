# import azure.functions as func
# import logging

# app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# # Run with func start -p 5000
# @app.function_name(name="HttpExample")
# @app.route(route="http_trigger")
# def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )

import azure.functions as func
from hello_function import handle_hello_request
from sensor_data_function import handle_sensor_request

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
