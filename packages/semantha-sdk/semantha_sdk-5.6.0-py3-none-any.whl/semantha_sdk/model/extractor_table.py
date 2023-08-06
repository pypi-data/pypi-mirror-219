
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.column import Column
from semantha_sdk.model.extractor_class_overview import ExtractorClassOverview
from typing import List
from typing import Optional


@dataclass(frozen=True)
class ExtractorTable(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    id: Optional[str]
    name: str
    class_id: str
    type: str
    columns: Optional[List[Column]]
    end_names: Optional[List[str]]
    start_before: Optional[List[str]]
    end_after: Optional[List[str]]
    used_classes: Optional[List[ExtractorClassOverview]]
    column_names: Optional[List[str]]

ExtractorTableSchema = class_schema(ExtractorTable, base_schema=SemanthaSchema)
