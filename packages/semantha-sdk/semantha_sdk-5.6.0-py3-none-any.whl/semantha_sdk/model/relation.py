
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.field import Field
from semantha_sdk.model.relation_condition import RelationCondition
from typing import List
from typing import Optional


@dataclass(frozen=True)
class Relation(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    id: Optional[str]
    name: str
    conditions: List[RelationCondition]
    parent: RelationCondition
    source: Optional[List[Field]]

RelationSchema = class_schema(Relation, base_schema=SemanthaSchema)
