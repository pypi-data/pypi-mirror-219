import os
import requests
import urllib.parse
from http import HTTPStatus
from typing import Optional, Union

from osim_utils.logger import get_logger
from osim_utils.constants import ror_id2site
from osim_utils.decorators import check_response, process_response
from osim_utils.exceptions import DataNotFoundError, DataValidationError
from osim_utils.common import chunk_list


class CrossRefClient:
    """
    Client for CrossRef API
    """

    def __init__(self, user_email: Optional[str] = None):
        self.session = requests.Session()
        self.logger = get_logger()
        self.user_email = user_email
        self.common_params = {"format": "json"}
        if user_email is None:
            try:
                self.user_email = os.environ["CROSSREF_EMAIL"]
            except KeyError:
                self.logger.warning(
                    f"Environment variable CROSSREF_EMAIL not defined. Requests will be made from the common pool"
                )

    @process_response
    @check_response(HTTPStatus.OK)
    def get(self, **kwargs):
        url = kwargs.pop("url")
        params = {
            "pid": self.user_email,
            "format": "json",
        } | kwargs.get("params", dict())
        r = self.session.get(url=url, params=params)
        return r

    def get_metadata_by_doi(self, doi):
        params = {"id": doi}
        return self.get(url="https://doi.crossref.org/servlet/query", params=params)
