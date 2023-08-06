
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import List
from typing import Optional


@dataclass(frozen=True)
class RuleOverview(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    id: Optional[str]
    name: str
    read_only: Optional[bool]
    rule_string: Optional[str]
    tags: Optional[List[str]]

RuleOverviewSchema = class_schema(RuleOverview, base_schema=SemanthaSchema)
