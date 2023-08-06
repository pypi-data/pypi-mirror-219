
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.expression import Expression
from typing import List
from typing import Optional


@dataclass(frozen=True)
class Rule(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    id: Optional[str]
    name: str
    comment: Optional[str]
    error: Optional[str]
    tags: Optional[List[str]]
    backward: Optional[bool]
    expression: Expression

RuleSchema = class_schema(Rule, base_schema=SemanthaSchema)
