"""Example 042: Use embedded signing with CFR Part 11"""

# eg042_list_status_changes.py
from datetime import datetime
from docusign_esign import EnvelopesApi
from flask import session
from ...docusign import create_api_client

class Eg042listStatusChangesEnvelopes:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        return {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
        }

    @staticmethod
    def worker(args, from_date, to_date=None, status=None):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        envelope_api = EnvelopesApi(api_client)

        from_date_iso = datetime.fromisoformat(from_date).isoformat()
        query_params = {'from_date': from_date_iso}

        if to_date:
            to_date_iso = datetime.fromisoformat(to_date).isoformat()
            query_params['to_date'] = to_date_iso

        if status:
            query_params['status'] = status

        results = envelope_api.list_status_changes(args['account_id'], **query_params)
        return results.to_dict()
