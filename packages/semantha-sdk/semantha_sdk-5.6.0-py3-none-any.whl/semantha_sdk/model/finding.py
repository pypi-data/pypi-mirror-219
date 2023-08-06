
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class Finding(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    status_code: Optional[int]
    severity: Optional[str]
    message: Optional[str]

FindingSchema = class_schema(Finding, base_schema=SemanthaSchema)
