
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.extractor import Extractor
from typing import List
from typing import Optional


@dataclass(frozen=True)
class ExtractorAttribute(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    name: str
    property_id: str
    datatype: str
    default_value: Optional[str]
    text_mode: Optional[str]
    formatter_id: Optional[str]
    text_types: Optional[List[str]]
    extractors: Optional[List[Extractor]]

ExtractorAttributeSchema = class_schema(ExtractorAttribute, base_schema=SemanthaSchema)
