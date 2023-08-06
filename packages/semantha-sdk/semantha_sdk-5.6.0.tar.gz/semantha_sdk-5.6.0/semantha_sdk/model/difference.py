
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class Difference(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    operation: Optional[str]
    text: Optional[str]

DifferenceSchema = class_schema(Difference, base_schema=SemanthaSchema)
