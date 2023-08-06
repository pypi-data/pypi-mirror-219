
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.extraction_area import ExtractionArea
from typing import Optional


@dataclass(frozen=True)
class TableInstance(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    type: Optional[str]
    extraction_area: Optional[ExtractionArea]

TableInstanceSchema = class_schema(TableInstance, base_schema=SemanthaSchema)
