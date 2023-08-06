from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.data_property import DataProperty
from semantha_sdk.model.data_property import DataPropertySchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient
from typing import List

class BulkmodelDatapropertiesEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/dataproperties"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)


    def get(
        self,
    ) -> List[DataProperty]:
        """
        Get all dataproperties
            This is the quiet version of  'get /api/domains/{domainname}/dataproperties'
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params).execute().to(DataPropertySchema)

    def post(
        self,
        body: List[DataProperty] = None,
    ) -> None:
        """
        Create one or more dataproperties
            This is the quiet version of  'post /api/domains/{domainname}/dataproperties'
        Args:
        body (List[DataProperty]): 
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            json=DataPropertySchema().dump(body),
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.as_none()

    
    
    