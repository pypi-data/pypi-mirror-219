
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.field import Field
from typing import List


@dataclass(frozen=True)
class RelationCondition(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    fields: List[Field]

RelationConditionSchema = class_schema(RelationCondition, base_schema=SemanthaSchema)
