from semantha_sdk.api.child_extractorclasses import ChildExtractorclassesEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.extractor_class import ExtractorClass
from semantha_sdk.model.extractor_class import ExtractorClassSchema
from semantha_sdk.rest.rest_client import RestClient

class ModelExtractorclassEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + f"/{self._id}"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
        id: str,
    ) -> None:
        super().__init__(session, parent_endpoint)
        self._id = id
        self.__extractorclasses = ChildExtractorclassesEndpoint(session, self._endpoint)

    @property
    def extractorclasses(self) -> ChildExtractorclassesEndpoint:
        return self.__extractorclasses

    def get(
        self,
    ) -> ExtractorClass:
        """
        Get an extractor class by id
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params).execute().to(ExtractorClassSchema)

    
    
    def delete(
        self,
    ) -> None:
        """
        Delete an extractor class by id
        """
        self._session.delete(
            url=self._endpoint,
        ).execute()

    def put(
        self,
        body: ExtractorClass
    ) -> ExtractorClass:
        """
        Update an extractor class by id
        """
        return self._session.put(
            url=self._endpoint,
            json=ExtractorClassSchema().dump(body)
        ).execute().to(ExtractorClassSchema)
