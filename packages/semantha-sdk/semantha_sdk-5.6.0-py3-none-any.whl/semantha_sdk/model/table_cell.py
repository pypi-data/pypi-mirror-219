
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class TableCell(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    text: Optional[str]

TableCellSchema = class_schema(TableCell, base_schema=SemanthaSchema)
