import requests
from http import HTTPStatus

from osim_utils.logger import get_logger
from osim_utils.decorators import check_response, process_response


class RorClient:
    """
    Client for ROR API
    """

    def __init__(self):
        self.base_endpoint = "https://api.ror.org/organizations"
        self.session = requests.Session()
        self.logger = get_logger()

    @process_response
    @check_response(HTTPStatus.OK)
    def get_organisation_by_id(self, ror_id: str) -> dict:
        """
        :param ror_id: supports both ROR id (04m01e293) and ROR url (https://ror.org/04m01e293)
        :return:
        """
        return self.session.get(url=f"{self.base_endpoint}/{ror_id.split('/')[-1]}")
