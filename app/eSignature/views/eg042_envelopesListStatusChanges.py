"""Example 042: Use embedded signing with CFR Part 11"""
# eg042_list_status_changes_blueprint.py
import json
from flask import Blueprint, render_template, request, jsonify, session
from ..examples.eg042_listStatusChangesEnvelopes import Eg042listStatusChangesEnvelopes
from ...consts import API_TYPE
from ...ds_config import DS_CONFIG

example_number = 42
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg042 = Blueprint(eg, __name__)

@eg042.route(f"/{eg}", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        status = request.form['status']
        storage_path = request.form['storage_path']

        if not from_date:
            return "Missing 'from_date' parameter", 400

        args = Eg042listStatusChangesEnvelopes.get_args()
        results = Eg042listStatusChangesEnvelopes.worker(args, from_date, to_date, status)

        # Save the results as a JSON file
        with open(storage_path, 'w') as outfile:
            json.dump(results, outfile)

        return jsonify(results)
    return render_template('eg042_envelopesListStatusChanges.html')

