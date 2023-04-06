from datetime import datetime, timedelta
import requests
from docusign_esign import EnvelopesApi
from flask import session

from ...docusign import create_api_client

from flask import Flask, request

app = Flask(__name__)

@app.route('/envelopes', methods=['GET'])
def get_envelopes():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    status = request.args.get('status')

    if not from_date:
        return "Missing 'from_date' parameter", 400

    results = worker(from_date=from_date, to_date=to_date, status=status)
    return str(results)

def worker(from_date, to_date=None, status=None):
    """
    Call the envelope status change method to list the envelopes
    that have changed within the specified date range and status
    """

    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = args['base_path']
    api_client.set_default_header("Authorization", "Bearer " + args['ds_access_token'])
    envelope_api = EnvelopesApi(api_client)

    # The Envelopes::listStatusChanges method has many options
    # See https://developers.docusign.com/esign-rest-api/reference/Envelopes/Envelopes/listStatusChanges

    # Use ISO 8601 date format
    from_date_iso = datetime.fromisoformat(from_date).isoformat()
    query_params = {'from_date': from_date_iso}

    if to_date:
        to_date_iso = datetime.fromisoformat(to_date).isoformat()
        query_params['to_date'] = to_date_iso

    if status:
        query_params['status'] = status

    results = envelope_api.list_status_changes(args['account_id'], **query_params)

    return results

if __name__ == "__main__":
    app.run()