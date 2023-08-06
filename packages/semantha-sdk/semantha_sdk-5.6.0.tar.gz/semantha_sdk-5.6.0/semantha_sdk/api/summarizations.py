from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient
from typing import List

class SummarizationsEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/summarizations"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)


    
    def post(
        self,
        texts: List[str] = None,
        topic: str = None,
    ) -> str:
        """
        
        Args:
        texts (List[str]): 
    topic (str): 
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            body={
                "texts": texts,
                "topic": topic,
            },
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.as_str()

    
    
    