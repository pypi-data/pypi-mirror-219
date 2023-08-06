from io import IOBase
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.language_detection import LanguageDetection
from semantha_sdk.model.language_detection import LanguageDetectionSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient

class LanguagesEndpoint(SemanthaAPIEndpoint):
    """ author semantha, this is a generated class do not change manually! TODO: resource.comment?"""

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/languages"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)


    
    def post(
        self,
        file: IOBase = None,
    ) -> LanguageDetection:
        """
        Identifies the language of the document and sends it back
            Input: Support of all input formats (PDF, Docx, Text, JSON (DocumentModel)
            
            Output: Detected Language
            
            Supported Languages:
            
            "ar“, "cs", "da", "de", "en", "es", "el", "fr", "fi", "hu", "hr",
            "it", "ja", "ko", "nl", "no", "pl", "pt", "ro", "ru", "sk", "sl",
            "sv", "tr", "zh-CN"
        Args:
        file (IOBase): Input document (left document).
        """
        q_params = {}
        response = self._session.post(
            url=self._endpoint,
            body={
                "file": file,
            },
            headers=RestClient.to_header(MediaType.JSON),
            q_params=q_params
        ).execute()
        return response.to(LanguageDetectionSchema)

    
    
    