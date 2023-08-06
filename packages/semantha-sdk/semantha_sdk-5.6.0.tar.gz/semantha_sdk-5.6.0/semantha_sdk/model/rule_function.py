
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class RuleFunction(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    name: Optional[str]
    min_arg_length: Optional[int]
    max_arg_length: Optional[int]
    type: Optional[str]

RuleFunctionSchema = class_schema(RuleFunction, base_schema=SemanthaSchema)
