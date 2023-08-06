
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from semantha_sdk.model.reference import Reference
from typing import List
from typing import Optional


@dataclass(frozen=True)
class MatrixRow(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    document_id: Optional[str]
    document_name: Optional[str]
    references: Optional[List[Reference]]

MatrixRowSchema = class_schema(MatrixRow, base_schema=SemanthaSchema)
