from datetime import datetime
import urllib
import requests

from typing import Optional, Any

from cqlpy._internal.logger import get_logger

from cqlpy._internal.exceptions import CqlPyValueError


FHIR_VERSION = "R4"
ROSETTA_BASE_URL = (
    f"https://api.rosetta.careevolution.com/terminology/v1/fhir/{FHIR_VERSION}"
)
ROSETTA_PAGE_SIZE = 250


class RosettaValuesetProvider:
    """
    A valueset provider that uses the [Rosetta terminology service](https://rosetta.careevolution.com).
    """

    def __init__(self, api_key: str):
        """
        Creates a new instance of the RosettaValuesetProvider class.

        ## Parameters

        - `api_key`: The API key to use when making requests to the Rosetta terminology service.
        """
        self._api_key = api_key
        self._logger = get_logger().getChild(self.__class__.__name__)

    def _get_valueset_url(
        self,
        name: Optional[str] = None,
        scope: Optional[str] = None,
        page_number: int = 0,
    ) -> str:
        extension = ""
        name_param = ""

        if scope is None and name is None:
            raise CqlPyValueError("Either scope or name must be provided")

        if scope:
            extension = f"&extension.scope={scope}"
        if name:
            valueset_id = urllib.parse.quote_plus(name)
            name_param = f"name={valueset_id}"

        url = f"{ROSETTA_BASE_URL}/ValueSet?{name_param}&page.num={page_number}&_count={ROSETTA_PAGE_SIZE}{extension}"

        return url

    def _get_request_headers(self, zip_encoding):
        header = {
            "X-API-Key": f"{self._api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return header

    def _request_valueset(self, url: str):
        start_time = datetime.now()

        headers = self._get_request_headers(False)
        response = requests.get(url=url, headers=headers)
        try:
            response.raise_for_status()
            response_json = response.json()
        except requests.exceptions.HTTPError as error:
            response_json = {}
            self._logger.error(
                f"RosettaValueSetProvider:_request_valueset, Error received: {str(error)}"
            )

        self._logger.info(
            f"RosettaValueSetProvider._request_valueset - Time to fetch valueset is {(datetime.now() - start_time).total_seconds()}"
        )
        return response_json

    def get_valueset(self, name: str, scope: Optional[str] = None) -> dict[str, Any]:
        self._logger.info(
            f"RosettaValueSetProvider.get_valueset, fetching valueset {scope if scope else 'scopeless'}:{name} from {ROSETTA_BASE_URL}"
        )

        json_response = self._request_valueset(
            self._get_valueset_url(
                name=name,
                scope=scope,
            )
        )

        if (
            json_response.get("resourceType", None) != "Bundle"
            or len(json_response.get("entry")) == 0
        ):
            self._logger.error(
                f"RosettaValueSetProvider.get_valueset - ValueSet for {scope if scope else 'scopeless'},{name} not found"
            )
            return {"resource": json_response}

        # if scope is not provided, we can receive more than one entry, returning the first one for now.
        entry = json_response.get("entry")[0]

        if entry["resource"]["resourceType"] != "ValueSet":
            raise Exception(
                f"ValueSet search returned unexpected resource {entry['resource']['resourceType']}"
            )

        return entry["resource"]

    def get_valuesets_in_scope(self, scope: str) -> list[dict[str, Any]]:
        self._logger.info(
            f"RosettaValueSetProvider.get_valuesets_in_scope, fetching valuesets in scope {scope} from {ROSETTA_BASE_URL}"
        )

        start_time = datetime.now()
        first_page_result = self._request_paged_valuesets_in_scope(scope=scope)

        resource_type = first_page_result.get("resourceType")

        if resource_type != "Bundle":
            self._logger.error(
                f"RosettaValueSetProvider.get_valuesets_in_scope - Invalid result when requesting valuesets in scope {scope}"
            )
            raise Exception(
                f"Invalid result when requesting valuesets in scope {scope}"
            )

        valuesets = []
        total = first_page_result.get("total", 0)

        number_of_pages = int(total / ROSETTA_PAGE_SIZE) + 1

        valuesets = first_page_result.get("entry", [])
        for page in range(1, number_of_pages + 1):
            json_response = self._request_paged_valuesets_in_scope(
                scope=scope, page=page
            )
            entries_on_this_page = json_response.get("entry", [])
            valuesets.extend(entries_on_this_page)

        self._logger.info(
            f"RosettaValueSetProvider.get_valuesets_in_scope - Time to fetch {len(valuesets)} valuesets is {(datetime.now() - start_time).total_seconds()}"
        )

        return valuesets

    def _request_paged_valuesets_in_scope(self, scope: str, page: int = 0):
        headers = self._get_request_headers(False)
        url = self._get_valueset_url(scope=scope, page_number=page)

        response = requests.get(url=url, headers=headers)

        return response.json()
