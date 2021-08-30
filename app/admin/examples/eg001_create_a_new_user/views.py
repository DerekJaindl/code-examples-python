"""Example 001: Create a new user"""

import json
from os import path

from flask import Blueprint, render_template, request, current_app
from docusign_admin.client.api_exception import ApiException

from app.error_handlers import process_error
from app.docusign import authenticate
from app.ds_config import DS_CONFIG

from .controller import Eg001Controller

eg = "eg001"  # Reference (and URL) for this example
eg001 = Blueprint(eg, __name__)

@eg001.route("/eg001", methods=["POST"])
@authenticate(eg=eg)
def get_user_data():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """

    controller = Eg001Controller()

    # 1. Get required arguments
    args = Eg001Controller.get_args(request)

    # 2. Call the worker method
    try:
        results = Eg001Controller.worker(controller, args)
        current_app.logger.info(f"ID of the created user: {results.id}")
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Create a new active eSignature user",
        h1="Create a new active eSignature user",
        message="Results from Users:createUser method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@eg001.route("/eg001", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """
    Responds with the form for the example
    """
    args = Eg001Controller.get_args(request)
    
    try:
        profiles = Eg001Controller.get_permission_profiles(args)
        groups = Eg001Controller.get_groups(args)

    except ApiException as err:
        return process_error(err)

    # Render the response
    return render_template(
        "eg001_create_a_new_user.html",
        title="Create a new active eSignature user",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["admin_github_url"] + path.basename(
            path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
        permission_profiles=profiles,
        groups=groups
    )
