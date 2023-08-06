import os
import requests
import urllib.parse
from http import HTTPStatus
from typing import Optional

from osim_utils.logger import get_logger
from osim_utils.constants import ror_id2site
from osim_utils.decorators import check_response, process_response
from osim_utils.common import chunk_list


class OpenAlexClient:
    """
    Client for OpenAlex API
    """

    max_page_size = 50

    def __init__(self):
        self.base_endpoint = "https://api.openalex.org"
        self.works_endpoint = f"{self.base_endpoint}/works"
        self.session = requests.Session()
        self.logger = get_logger()

        req_env_var = "OpenAlexRequester"
        self.default_headers = dict()
        try:
            self.default_headers["User-agent"] = f"mailto:{os.environ[req_env_var]}"
        except KeyError:
            self.logger.warning(
                f"Environment variable {req_env_var} not defined. Requests will be made from the common pool (see  "
                f"https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication#the-polite-pool "
                f"for details)"
            )

    @process_response
    @check_response(HTTPStatus.OK)
    def get(self, url, **kwargs):
        headers = self.default_headers | kwargs.get("headers", dict())
        params = kwargs.get("params")
        return self.session.get(url, headers=headers, params=params)

    def get_work_by_doi(self, doi: str, **kwargs) -> dict:
        """
        Queries works by doi
        Args:
            doi: The doi of the publication we are querying for
            **kwargs: additional parameters to be passed to the OpenAlex API

        Returns: OpenAlex API response
        """
        return self.get(
            f"{self.works_endpoint}/doi:{urllib.parse.quote(doi)}", **kwargs
        )

    def get_works_by_doi_list(self, dois: list[str], **kwargs) -> dict:
        """
        Retrieves up to 50 works by querying for a list of dois
        Args:
            dois: list of dois to be queried
            **kwargs: additional parameters to be passed to the OpenAlex API

        Returns: OpenAlex API response
        """
        quoted_dois = [urllib.parse.quote(x) for x in dois]
        sublists = chunk_list(quoted_dois, self.max_page_size)
        for sl in sublists:
            query = "|".join(sl)
            params = {"filter": f"doi:{query}", "per-page": self.max_page_size}
            yield self.get(self.works_endpoint, params=params, **kwargs)

    def get_embl_works(self, filters: dict, **kwargs) -> dict:
        """
        Queries works associated with any of the EMBL ROR ids in ror_id2site

        Args:
            filters: additional filters to apply to query
                (see https://docs.openalex.org/how-to-use-the-api/get-lists-of-entities/filter-entity-lists)
            **kwargs: additional parameters to be passed to the OpenAlex API

        Returns:

        """
        filter_str = f"institutions.ror:{'|'.join(ror_id2site.keys())}"
        for k, v in filters.items():
            filter_str += f",{k}:{v}"
        params = {"filter": filter_str} | kwargs.pop("params", dict())
        return self.get(self.works_endpoint, params=params, **kwargs)

    def get_all_embl_works(self, filters: dict, **kwargs) -> dict:
        """
        Convenience method to get and return all results matching filter.
        In other words, this method loops through all pages of API results to return
        the total.

        Args:
            filters: additional filters to apply to query
                (see https://docs.openalex.org/how-to-use-the-api/get-lists-of-entities/filter-entity-lists)
            **kwargs: additional parameters to be passed to the OpenAlex API
        """
        cursor = "*"
        params = {"per-page": 200} | kwargs.pop("params", dict())
        results = list()
        while cursor:
            params.update(cursor=cursor)
            r = self.get_embl_works(filters=filters, params=params)
            results += r["results"]
            cursor = r["meta"]["next_cursor"]
        return {
            "meta": r["meta"],
            "results": results,
        }

    def get_works_by_orcids(
        self, orcids: list[str], filters: Optional[dict] = None, **kwargs
    ) -> dict:
        cursor = "*"
        filter_str = f"author.orcid:{'|'.join(orcids)}"
        if filters:
            for k, v in filters.items():
                filter_str += f",{k}:{v}"
        params = (
            {"filter": filter_str} | {"per-page": 200} | kwargs.pop("params", dict())
        )
        results = list()
        while cursor:
            params.update(cursor=cursor)
            r = self.get(self.works_endpoint, params=params, **kwargs)
            results += r["results"]
            cursor = r["meta"]["next_cursor"]
        return {
            "meta": r["meta"],
            "results": results,
        }
