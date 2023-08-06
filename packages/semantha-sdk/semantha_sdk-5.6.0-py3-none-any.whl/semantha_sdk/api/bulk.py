from semantha_sdk.api.bulk_domains import BulkDomainsEndpoint
from semantha_sdk.api.bulk_model import BulkModelEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.rest.rest_client import RestClient

class BulkEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/bulk"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)
        self.__domains = BulkDomainsEndpoint(session, self._endpoint)
        self.__model = BulkModelEndpoint(session, self._endpoint)

    @property
    def domains(self) -> BulkDomainsEndpoint:
        return self.__domains
    @property
    def model(self) -> BulkModelEndpoint:
        return self.__model

    
    
    
    
    