import asyncio
import json

import aiohttp
from fastapi import APIRouter

# app = APIRouter()


async def get_deribit_instruments():
    url = "https://test.deribit.com/api/v2/public/get_index_price?index_name=eth_usd"
    params = {"currency": "BTC"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()

                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            print(f"Ошибка при запросе к Deribit {e}")
            return None


if __name__ == "__main__":
    result = asyncio.run(get_deribit_instruments())
    if result:
        print(json.dumps(result, indent=4, ensure_ascii=False))
