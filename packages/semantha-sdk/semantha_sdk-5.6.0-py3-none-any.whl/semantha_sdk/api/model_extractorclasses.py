from semantha_sdk.api.model_extractorclass import ModelExtractorclassEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.extractor_class import ExtractorClass
from semantha_sdk.model.extractor_class import ExtractorClassSchema
from semantha_sdk.model.extractor_class_overview import ExtractorClassOverview
from semantha_sdk.model.extractor_class_overview import ExtractorClassOverviewSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient
from typing import List

class ModelExtractorclassesEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/extractorclasses"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)

    def __call__(
            self,
            id: str,
    ) -> ModelExtractorclassEndpoint:
        return ModelExtractorclassEndpoint(self._session, self._endpoint, id)

    def get(
        self,
    ) -> List[ExtractorClassOverview]:
        """
        Get all extractor classes
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params).execute().to(ExtractorClassOverviewSchema)

    def post(
        self,
        body: ExtractorClass = None,
    ) -> ExtractorClass:
        """
        Create an extractor class
        Args:
        body (ExtractorClass): 
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            json=ExtractorClassSchema().dump(body),
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.to(ExtractorClassSchema)

    
    def delete(
        self,
    ) -> None:
        """
        Delete all extractorclasses
        """
        self._session.delete(
            url=self._endpoint,
        ).execute()

    def put(
        self,
        body: ExtractorClassOverview
    ) -> None:
        """
        
        """
        return self._session.put(
            url=self._endpoint,
            json=ExtractorClassOverviewSchema().dump(body)
        ).execute().as_none()
