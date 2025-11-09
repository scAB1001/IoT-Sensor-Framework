# import azure.functions as func
import logging

def handle_hello_request(req) -> str:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return f"Hello, {name}. This HTTP triggered function executed successfully."
    else:
        return "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response."
