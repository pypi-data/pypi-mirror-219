
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class InstanceOverview(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    id: Optional[str]
    name: str
    read_only: Optional[bool]
    class_name: Optional[str]
    class_id: Optional[str]

InstanceOverviewSchema = class_schema(InstanceOverview, base_schema=SemanthaSchema)
