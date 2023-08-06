
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class LanguageDetection(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    language: Optional[str]

LanguageDetectionSchema = class_schema(LanguageDetection, base_schema=SemanthaSchema)
