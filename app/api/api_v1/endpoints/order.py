from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.depends import get_db
from app.crud.order import orders
from app.shemas import error, order

router = APIRouter()


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": list[order.OrderDto], "description": "ok"},
    },
)
def get_all_orders(
    limit: int = 1,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[order.OrderDto]:
    return orders.get_all_obj(db, limit, offset)


@router.post(
    "",
    responses={
        status.HTTP_200_OK: {"model": list[order.OrderDto], "description": "ok"},
    },
)
def create_orders(
    body: order.CreateOrderRequest,
    db: Session = Depends(get_db),
) -> list[order.OrderDto]:
    return orders.create_orders(db, body.orders)


@router.post(
    "/complete",
    responses={
        status.HTTP_200_OK: {"model": list[order.OrderDto], "description": "ok"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "bad request",
            "model": error.BadRequestResponse,
        },
    },
)
def create_completed_order(
    body: order.CompleteOrderRequestDto,
    db: Session = Depends(get_db),
) -> list[order.OrderDto]:
    try:
        return orders.create_completed_orders(db, body.complete_info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/{order_id}",
    responses={
        status.HTTP_200_OK: {"model": order.OrderDto, "description": "ok"},
        status.HTTP_404_NOT_FOUND: {
            "description": "not found",
            "model": error.NotFoundResponse,
        },
    },
)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
):
    if order := orders.get_obj_by_id(db, order_id):
        return order.to_dict()
    detail = f"Закза с id={order_id} не найден"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
