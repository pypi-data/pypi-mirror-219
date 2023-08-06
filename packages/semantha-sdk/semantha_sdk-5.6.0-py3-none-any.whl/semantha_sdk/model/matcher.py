
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema



@dataclass(frozen=True)
class Matcher(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    type: str
    value: str

MatcherSchema = class_schema(Matcher, base_schema=SemanthaSchema)
