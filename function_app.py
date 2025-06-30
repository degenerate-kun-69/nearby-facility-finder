import azure.functions as func
import logging
import os
from Facility_function.handler import handle_facility_request  # <- updated import

app = func.FunctionApp()

@app.route(route="facility_function", auth_level=func.AuthLevel.ANONYMOUS)
def facility_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Received HTTP request.')

    address = req.params.get('address')
    if not address:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        address = req_body.get('address')

    if not address:
        # Serve HTML if no address is provided
        html_path = os.path.join(os.path.dirname(__file__), 'static', 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return func.HttpResponse(html_content, mimetype="text/html")

    try:
        result = handle_facility_request(address)
        return func.HttpResponse(result, status_code=200)
    except Exception as e:
        logging.error(f"Handler error: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
