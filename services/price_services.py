from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select

from core.setup import async_session_factory
from models.price_models import PriceHistory
from schemas.price_schemas import PriceRead
from services.deribit_services import get_deribit_btc_usd, get_deribit_eth_usd


def ticker_validation(ticker: str):
    ticker = ticker.lower().strip()
    if ticker not in ["btc", "bitcoin", "ethereum", "eth"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticker not found",
        )
    return ticker


async def get_all_prices_service(ticker: str) -> List[PriceRead]:
    validated_ticker = ticker_validation(ticker)
    async with async_session_factory() as session:
        query = select(PriceHistory).where(PriceHistory.ticker == validated_ticker)
        res = await session.scalars(query)
        prices = res.all()

        return [PriceRead.model_validate(price) for price in prices]


async def get_latest_price_service(ticker: str) -> PriceRead:
    validated_ticker = ticker_validation(ticker)
    async with async_session_factory() as session:
        query = (
            select(PriceHistory)
            .where(PriceHistory.ticker == validated_ticker)
            .order_by(PriceHistory.timestamp.desc())
        )
        res = await session.scalars(query)
        price = res.first()
        if price is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No prices inside the database",
            )
        return PriceRead.model_validate(price)


async def get_prices_by_date_service(
    ticker: str, start_ts: int, end_ts: int
) -> List[PriceRead]:
    validated_ticker = ticker_validation(ticker)
    async with async_session_factory() as session:
        query = (
            select(PriceHistory)
            .where(
                PriceHistory.ticker == validated_ticker,
                PriceHistory.timestamp >= start_ts,
                PriceHistory.timestamp <= end_ts,
            )
            .order_by(PriceHistory.timestamp.asc())
        )

        result = await session.scalars(query)
        prices = result.all()
        return [PriceRead.model_validate(price) for price in prices]


async def create_price_service(ticker: str) -> PriceRead:
    validated_ticker = ticker_validation(ticker)
    async with async_session_factory() as session:
        match validated_ticker:
            case "bitcoin" | "btc":
                price = await get_deribit_btc_usd()
            case "ethereum" | "eth":
                price = await get_deribit_eth_usd()
        new_price = PriceHistory(ticker=validated_ticker, price=price)  # type: ignore
        session.add(new_price)

        await session.commit()
        await session.refresh(new_price)

        return PriceRead.model_validate(new_price)
