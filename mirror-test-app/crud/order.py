import random
from datetime import date
from typing import Sequence, Annotated
from fastapi import HTTPException, status, Query
from sqlalchemy import select, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, load_only, with_loader_criteria

from core.models import Order, DogWalker
from core.schemas.order import OrderCreate


async def get_all_orders(
    session: AsyncSession, walk_date: date | None
) -> Sequence[Order]:
    stmt = select(Order).options(joinedload(Order.dog_walker)).order_by(Order.walk_date)

    if walk_date:
        stmt = stmt.filter(cast(Order.walk_date, Date) == walk_date)

    result = await session.scalars(stmt)
    return result.all()


async def create_order(session: AsyncSession, order_create: OrderCreate) -> Order:
    order = Order(**order_create.model_dump())

    stmt = (
        select(DogWalker)
        .options(
            selectinload(DogWalker.orders).options(load_only(Order.id)),
            with_loader_criteria(
                Order,
                cast(Order.walk_date, Date)
                == order.walk_date.date(),  # берем заказы только на указанную дату
            ),
        )
        .filter(
            ~DogWalker.orders.any(Order.walk_date == order.walk_date)
        )  # если выгульщик занят, то исключаем
    )

    result = await session.scalars(stmt)
    available_dog_walkers = result.all()

    if not available_dog_walkers:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Нет свободных выгульщиков на {order.walk_date}",
        )

    random.shuffle(available_dog_walkers)  # берем случайного из самых свободных
    dog_walker = min(available_dog_walkers, key=lambda dw: len(dw.orders))
    order.dog_walker = dog_walker

    session.add(order)
    await session.commit()
    await session.refresh(order, attribute_names=["dog_walker"])
    return order
