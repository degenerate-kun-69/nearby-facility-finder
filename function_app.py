import azure.functions as func
import logging
import os
from Facility_function.handler import handle_facility_request
from dotenv import load_dotenv
load_dotenv()
app = func.FunctionApp()
#decorator to register http trigger with no auth needed
@app.route(route="facility_function", auth_level=func.AuthLevel.ANONYMOUS)

def facility_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f"Received {req.method} request at {req.url}")

    address = req.params.get('address') #extract param from the query string
    if not address:
        try:
            req_body = req.get_json()
        except ValueError: # to catch malformed JSON
            req_body = {} #default to empty dict if JSON is malformed
        address = req_body.get('address') #extract addressfrom payload

    if not address:
        # Serve HTML if no address is provided, made this to automatically serve the HTML page
        html_path = os.path.join(os.path.dirname(__file__), 'static', 'index.html') #abs path to index.html
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return func.HttpResponse(html_content, mimetype="text/html")

    try:
        result = handle_facility_request(address) #call func in facility_function.handler
        return func.HttpResponse(result, status_code=200) #plaintext response if success
    except Exception as e:
        logging.error(f"Handler error: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
