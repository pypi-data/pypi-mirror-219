from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.synonym import Synonym
from semantha_sdk.model.synonym import SynonymSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient
from typing import List

class BulkmodelSynonymsEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/synonyms"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)


    
    def post(
        self,
        body: List[Synonym] = None,
    ) -> None:
        """
        Create one or more synonyms
            This is the quiet version of  'post /api/domains/{domainname}/synonyms'
        Args:
        body (List[Synonym]): 
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            json=SynonymSchema().dump(body),
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.as_none()

    
    
    