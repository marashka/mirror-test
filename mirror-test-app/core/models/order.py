from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.base import int_pk


class Order(Base):
    id: Mapped[int_pk]
    apartment_number: Mapped[int] = mapped_column(
        nullable=False, comment="Номер квартиры заказчика"
    )
    pet_name: Mapped[str] = mapped_column(nullable=False, comment="Кличка питомца")
    pet_breed: Mapped[str] = mapped_column(nullable=False, comment="Порода питомца")
    walk_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, comment="Дата и время начала прогулки"
    )

    dog_walker_id: Mapped[int] = mapped_column(
        ForeignKey("dog_walkers.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID выгульщика",
    )

    dog_walker: Mapped["DogWalker"] = relationship(back_populates="orders")

    __table_args__ = (
        UniqueConstraint(
            "walk_date",
            "dog_walker_id",
            name="unique_order",
        ),
    )
