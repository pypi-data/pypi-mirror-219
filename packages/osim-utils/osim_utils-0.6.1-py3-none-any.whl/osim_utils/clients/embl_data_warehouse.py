import functools
import json
import os
import requests
from http import HTTPStatus

import osim_utils.exceptions as exc
from osim_utils.decorators import check_response, process_response
from osim_utils.logger import get_logger


class DataWareClient:
    """
    API client for EMBL's data warehouse API (Converis mirror)
    """

    def __init__(self):
        self.base_url = "https://xs-db.embl.de/v2/publications/"
        self.session = requests.Session()
        self.logger = get_logger()

        token_env_var = "DataWareHouseToken"
        self.default_headers = dict()
        try:
            self.default_headers[
                "Authorization"
            ] = f"Bearer {os.environ[token_env_var]}"
        except KeyError:
            raise exc.AuthenticationError(
                f"Environment variable {token_env_var} not defined. If you do not have an authorization"
                f"token for the Converis mirror dataset in EMBL's Data Warehouse API, please contact"
                f"Converis administrators."
            )

    @process_response
    @check_response(HTTPStatus.OK)
    def _get_all_pubs(self, **kwargs):
        headers = self.default_headers | kwargs.get("headers", dict())
        return self.session.get(self.base_url, headers=headers, params={"all": "true"})

    def get_all_publications(self, **kwargs):
        r = self._get_all_pubs(**kwargs)
        unique_pubs = list()
        processed_pubs = list()
        for owner in r:
            pubs = owner["publications"]
            for k, v in pubs.items():
                if (pub_id := v["id"]) not in processed_pubs:
                    processed_pubs.append(pub_id)
                    unique_pubs.append(v)
        return unique_pubs
