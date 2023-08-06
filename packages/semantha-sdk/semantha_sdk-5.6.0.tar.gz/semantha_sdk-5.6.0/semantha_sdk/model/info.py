
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class Info(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    title: Optional[str]
    vendor: Optional[str]
    time: Optional[str]
    git: Optional[str]
    version: Optional[str]

InfoSchema = class_schema(Info, base_schema=SemanthaSchema)
