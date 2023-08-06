
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.extractor import Extractor
from typing import List
from typing import Optional


@dataclass(frozen=True)
class ExtractorClassOverview(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    id: Optional[str]
    name: str
    class_id: str
    matcher: Optional[List[Extractor]]
    metadata: Optional[str]
    attributes: Optional[List[str]]

ExtractorClassOverviewSchema = class_schema(ExtractorClassOverview, base_schema=SemanthaSchema)
