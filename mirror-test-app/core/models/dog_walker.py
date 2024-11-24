from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.base import int_pk


class DogWalker(Base):
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(nullable=False, comment="Имя выгульщика собак")
    phone_number: Mapped[str] = mapped_column(
        String(15), nullable=False, comment="Контактный номер выгульщика собак"
    )
    orders: Mapped[list["Order"]] = relationship(back_populates="dog_walker")
