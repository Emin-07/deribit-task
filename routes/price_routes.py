import time
from typing import Annotated, List

from fastapi import APIRouter, Query

from schemas.price_schemas import PriceRead
from services.price_services import (
    get_all_prices_service,
    get_latest_price_service,
    get_prices_by_date_service,
)

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/", response_model=List[PriceRead])
async def get_all_prices(
    ticker: Annotated[str, Query(..., examples=["eth", "ethereum", "btc", "bitcoin"])],
):
    return await get_all_prices_service(ticker)


@router.get("/latest", response_model=PriceRead)
async def get_latest_price(
    ticker: Annotated[str, Query(..., examples=["eth", "ethereum", "btc", "bitcoin"])],
):
    return await get_latest_price_service(ticker)


@router.get("/history", response_model=List[PriceRead])
async def get_prices_by_date(
    ticker: Annotated[str, Query(..., examples=["eth", "ethereum", "btc", "bitcoin"])],
    start_ts: Annotated[int, Query(..., description="Start UNIX timestamp")],
    end_ts: Annotated[int | None, Query(description="End UNIX timestamp")] = None,
):
    if end_ts is None:
        end_ts = int(time.time())

    return await get_prices_by_date_service(
        ticker=ticker, start_ts=start_ts, end_ts=end_ts
    )


# FIXME:  good for testing without celery
# @router.post("/", response_model=PriceRead)
# async def create_new_price(
#     ticker: Annotated[str,Query(..., examples=["eth", "ethereum", "btc", "bitcoin"])],
# ):
#     return await create_price_service(ticker)
