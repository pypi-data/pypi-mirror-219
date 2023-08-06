from io import IOBase
from semantha_sdk.api.modelont_instance import ModelontInstanceEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.instance import Instance
from semantha_sdk.model.instance import InstanceSchema
from semantha_sdk.model.instance_overview import InstanceOverview
from semantha_sdk.model.instance_overview import InstanceOverviewSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient
from typing import List

class ModelontInstancesEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/instances"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)

    def __call__(
            self,
            id: str,
    ) -> ModelontInstanceEndpoint:
        return ModelontInstanceEndpoint(self._session, self._endpoint, id)

    def get(
        self,
    ) -> List[InstanceOverview]:
        """
        Get all instances
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params).execute().to(InstanceOverviewSchema)
    def get_as_xlsx(
        self,
    ) -> IOBase:
        """
        Get all instances
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params).execute().as_bytesio()

    def post(
        self,
        body: Instance = None,
    ) -> Instance:
        """
        Create an instance
        Args:
        body (Instance): 
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            json=InstanceSchema().dump(body),
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.to(InstanceSchema)

    def patch(
        self,
        file: IOBase
    ) -> IOBase:
        """
        Update all instances
        """
        return self._session.patch(
            url=self._endpoint,
            json=file
        ).execute().as_none()

    def delete(
        self,
    ) -> None:
        """
        Delete all instances
        """
        self._session.delete(
            url=self._endpoint,
        ).execute()

    