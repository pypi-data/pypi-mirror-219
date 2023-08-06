
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import List
from typing import Optional


@dataclass(frozen=True)
class CurrentUser(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    name: Optional[str]
    valid_until: Optional[int]
    roles: Optional[List[str]]

CurrentUserSchema = class_schema(CurrentUser, base_schema=SemanthaSchema)
