from typing import Annotated

from sqlalchemy import MetaData
from sqlalchemy.orm import (
    mapped_column,
    as_declarative,
    declared_attr,
)

from core.config import settings
from utils.case_converter import camel_case_to_snake_case

int_pk = Annotated[int, mapped_column(primary_key=True)]


@as_declarative()
class Base:
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
