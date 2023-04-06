"""Example 042: Use embedded signing with CFR Part 11"""

from docusign_esign.client.api_exception import ApiException
from flask import render_template, request, Blueprint, current_app as app, session

from ..examples.list_status_changes import worker
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 42  # Change this to a new example number
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg042 = Blueprint(eg, __name__)

@eg042.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def list_status_changes():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the results
    """
    try:
        # 1. Get required arguments
        from_date = request.form.get("from_date")
        to_date = request.form.get("to_date")
        status = request.form.get("status")

        if not from_date:
            return "Missing 'from_date' parameter", 400

        args = {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "ds_access_token": session["ds_access_token"],
        }

        # 2. Call the worker method
        results = worker(from_date=from_date, to_date=to_date, status=status, args=args)

    except ApiException as err:
        return process_error(err)

    # 3. Render the results
    return render_template("eSignature/eg042_list_status_changes.html", results=results)

@eg042.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)
    return render_template(
        "eSignature/eg042_list_status_changes.html",
        title=example["ExampleName"],
        example=example,
        source_file="list_status_changes.py",
        source_url=DS_CONFIG["github_example_url"] + "list_status_changes.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

