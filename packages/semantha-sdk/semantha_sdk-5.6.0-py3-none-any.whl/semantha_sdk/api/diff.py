from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.difference import Difference
from semantha_sdk.model.difference import DifferenceSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient
from typing import List

class DiffEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/diff"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)


    
    def post(
        self,
        left: str = None,
        right: str = None,
    ) -> List[Difference]:
        """
        Create diff on structural basis
        Args:
        left (str): The base for creating a diff
    right (str): The changed text which gets compared to „left“ text.
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            body={
                "left": left,
                "right": right,
            },
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.to(DifferenceSchema)

    
    
    