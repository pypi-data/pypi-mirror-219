from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.named_entity import NamedEntity
from semantha_sdk.model.named_entity import NamedEntitySchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient
from typing import List

class BulkmodelNamedentitiesEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/namedentities"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)


    
    def post(
        self,
        body: List[NamedEntity] = None,
    ) -> None:
        """
        Create one or more named entities
            This is the quiet version of  'post /api/domains/{domainname}/namedentities'
        Args:
        body (List[NamedEntity]): 
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            json=NamedEntitySchema().dump(body),
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.as_none()

    
    
    