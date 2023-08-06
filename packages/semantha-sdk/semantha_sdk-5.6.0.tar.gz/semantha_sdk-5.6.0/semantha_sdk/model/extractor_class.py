
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.extractor import Extractor
from semantha_sdk.model.extractor_attribute import ExtractorAttribute
from semantha_sdk.model.table import Table
from typing import List
from typing import Optional


@dataclass(frozen=True)
class ExtractorClass(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    id: Optional[str]
    name: str
    class_id: str
    matcher: Optional[List[Extractor]]
    metadata: Optional[str]
    attributes: Optional[List[ExtractorAttribute]]
    tables: Optional[List[Table]]
    document_type: Optional[str]
    split_document_extractor: Optional[str]

ExtractorClassSchema = class_schema(ExtractorClass, base_schema=SemanthaSchema)
