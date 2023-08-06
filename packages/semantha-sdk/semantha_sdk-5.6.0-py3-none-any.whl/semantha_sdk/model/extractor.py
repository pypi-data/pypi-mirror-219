
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.matcher import Matcher
from semantha_sdk.model.range import Range
from typing import Optional


@dataclass(frozen=True)
class Extractor(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    type: str
    value: str
    combination_type: Optional[str]
    range: Optional[Range]
    start: Optional[Matcher]
    end: Optional[Matcher]

ExtractorSchema = class_schema(Extractor, base_schema=SemanthaSchema)
