from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.rule import Rule
from semantha_sdk.model.rule import RuleSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient
from typing import List

class BulkmodelRulesEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/rules"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)


    def get(
        self,
    ) -> List[Rule]:
        """
        Get a rule
            This is the quiet version of 'get /api/model/domains/{domainname}/rules'
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params).execute().to(RuleSchema)

    def post(
        self,
        body: List[Rule] = None,
    ) -> None:
        """
        Create a rule
            This is the quiet version of 'post /api/model/domains/{domainname}/rules'
        Args:
        body (List[Rule]): 
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            json=RuleSchema().dump(body),
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.as_none()

    
    
    