from datetime import date
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy.ext.asyncio import AsyncSession


from core.models import db_helper
from core.schemas.order import (
    OrderRead,
    OrderCreate,
)
from crud import order as orders_crud

router = APIRouter(tags=["Orders"])


@router.get("", response_model=list[OrderRead])
async def get_orders(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    walk_date: Annotated[date | None, Query(description="Дата прогулки")] = None,
):

    orders = await orders_crud.get_all_orders(session=session, walk_date=walk_date)
    return orders


@router.post("", response_model=OrderRead)
async def create_orders(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_create: OrderCreate,
):

    order = await orders_crud.create_order(session=session, order_create=order_create)
    return order
