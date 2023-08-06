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


class SherpaClient:
    """
    Client for JISC Sherpa APIs
    """

    def __init__(self, api_key: Optional[str] = None):
        self.base_endpoint = "https://v2.sherpa.ac.uk/cgi/retrieve"
        self.api_key = api_key
        if api_key is None:
            try:
                self.api_key = os.environ["SHERPA_KEY"]
            except KeyError:
                raise DataNotFoundError(
                    "Could not find API key for JISC Sherpa services; please store the key "
                    "value in environment variable SHERPA_KEY or pass the key value directly as attribute api_key"
                    "when instantiating this SherpaClient"
                )
        self.session = requests.Session()
        self.logger = get_logger()

    @process_response
    @check_response(HTTPStatus.OK)
    def get(self, **kwargs):
        params = {
            "api-key": self.api_key,
            "item-type": "publication",
            "format": "Json",
        } | kwargs.get("params", dict())
        r = self.session.get(url=self.base_endpoint, params=params)
        return r

    def get_journal_by_issn(self, issn: Union[str, list[str]]) -> dict:
        if isinstance(issn, str):
            params = {"filter": f'[["issn", "equals", "{issn}"]]'}
            r = self.get(params=params)
        elif isinstance(issn, list):
            params = {"filter": f'[["issn", "equals", "{issn[0]}"]]'}
            r = self.get(params=params)
            try:
                return r["items"][0]
            except IndexError:
                params = {"filter": f'[["issn", "equals", "{issn[1]}"]]'}
                r = self.get(params=params)
        else:
            raise DataValidationError(
                f"Attribute issn has to be a str or list; {type(issn)} found"
            )
        try:
            return r["items"][0]
        except IndexError:
            return dict()

    def get_journal_by_title(self, title: str) -> dict:
        params = {"filter": f'[["title", "equals", "{title}"]]'}
        r = self.get(params=params)
        try:
            return r["items"][0]
        except IndexError:
            return dict()
