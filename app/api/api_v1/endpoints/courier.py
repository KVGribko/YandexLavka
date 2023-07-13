from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.depends import get_db
from app.crud.courier import couriers
from app.shemas import courier, error

router = APIRouter()


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": courier.GetCouriersResponse, "description": "ok"},
    },
)
def get_all_couriers(
    limit: int = 1,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> courier.GetCouriersResponse:
    return courier.GetCouriersResponse(
        couriers=couriers.get_all_obj(db, limit, offset),
        limit=limit,
        offset=offset,
    )


@router.post(
    "",
    responses={
        status.HTTP_200_OK: {
            "model": courier.CreateCouriersResponse,
            "description": "ok",
        },
    },
)
def create_couriers(
    body: courier.CreateCourierRequest,
    db: Session = Depends(get_db),
) -> courier.CreateCouriersResponse:
    return courier.CreateCouriersResponse(
        couriers=couriers.create_couriers(db, body.couriers)
    )


@router.get(
    "/{courier_id}",
    responses={
        status.HTTP_200_OK: {"model": courier.CourierDto, "description": "ok"},
        status.HTTP_404_NOT_FOUND: {
            "description": "not found",
            "model": error.NotFoundResponse,
        },
    },
)
def get_courier_by_id(
    courier_id: int,
    db: Session = Depends(get_db),
):
    if courier := couriers.get_obj_by_id(db, courier_id):
        return courier.to_dict()
    detail = f"Курьер с id={courier_id} не найден"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


@router.get(
    "/meta-info/{courier_id}",
    responses={
        status.HTTP_200_OK: {
            "model": courier.GetCourierMetaInfoResponse,
            "description": "ok",
        },
    },
)
def get_courier_rating(
    courier_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
) -> courier.GetCourierMetaInfoResponse:
    return couriers.get_meta_info(db, courier_id, start_date, end_date)
