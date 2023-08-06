from semantha_sdk.api.bulkmodel_domains import BulkmodelDomainsEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.rest.rest_client import RestClient

class BulkModelEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/model"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)
        self.__domains = BulkmodelDomainsEndpoint(session, self._endpoint)

    @property
    def domains(self) -> BulkmodelDomainsEndpoint:
        return self.__domains

    
    
    
    
    