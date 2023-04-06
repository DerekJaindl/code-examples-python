"""Example 042: Use embedded signing with CFR Part 11"""

import os
import json
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from docusign_esign import ApiClient, EnvelopesApi
from ds_config import DS_CONFIG

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        status = request.form['status']

        if not from_date:
            return "Missing 'from_date' parameter", 400

        results = list_status_changes(from_date, to_date, status)
        return jsonify(results)
    return render_template('index.html')


def list_status_changes(from_date, to_date=None, status=None):
    api_client = ApiClient()
    api_client.host = DS_CONFIG['base_path']
    api_client.set_default_header("Authorization", f"Bearer {DS_CONFIG['access_token']}")
    envelope_api = EnvelopesApi(api_client)

    from_date_iso = datetime.fromisoformat(from_date).isoformat()
    query_params = {'from_date': from_date_iso}

    if to_date:
        to_date_iso = datetime.fromisoformat(to_date).isoformat()
        query_params['to_date'] = to_date_iso

    if status:
        query_params['status'] = status

    results = envelope_api.list_status_changes(DS_CONFIG['account_id'], **query_params)
    return results.to_dict()


if __name__ == "__main__":
    app.run()

