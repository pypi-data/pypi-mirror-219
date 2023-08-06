
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.file_reference import FileReference
from semantha_sdk.model.rect import Rect
from typing import Optional


@dataclass(frozen=True)
class ExtractionArea(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    file: Optional[FileReference]
    rect: Optional[Rect]

ExtractionAreaSchema = class_schema(ExtractionArea, base_schema=SemanthaSchema)
