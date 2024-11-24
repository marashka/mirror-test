from datetime import datetime

from pydantic import BaseModel, field_validator
from core.config import settings
from core.schemas.dog_walker import DogWalkerRead


class OrderBase(BaseModel):
    apartment_number: int
    pet_name: str
    pet_breed: str
    walk_date: datetime


class OrderCreate(OrderBase):

    @field_validator("walk_date", mode="before")
    def check_date_format(cls, value: str) -> str:
        datetime.strptime(str(value), "%Y-%m-%d %H:%M")
        return value

    @field_validator("walk_date")
    def check_past_date(cls, value: datetime) -> datetime:
        if value < datetime.now():
            raise ValueError("walk_date must not be in the past.")
        return value

    @field_validator("walk_date")
    def check_walk_time(cls, value: datetime) -> datetime:
        if value.hour < settings.order.earliest_walk_hour:
            raise ValueError(
                f"Walk date must not be earlier than {settings.order.earliest_walk_hour}:00 AM."
            )

        if value.hour > settings.order.latest_walk_hour:
            raise ValueError(
                f"Walk date must not be later than {settings.order.latest_walk_hour}:00 PM."
            )
        return value

    @field_validator("walk_date")
    def check_minutes(cls, value: datetime) -> datetime:
        if value.minute not in settings.order.allowed_minutes:
            raise ValueError("walk_date must have minutes as 00 or 30.")
        return value


class OrderRead(OrderBase):
    id: int
    dog_walker: DogWalkerRead
