import asyncio

import aiohttp


async def get_deribit_crypto_price(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()

                data = await response.json()
                return float(data["result"]["index_price"])
        except aiohttp.ClientError as e:
            print(f"Ошибка при запросе к Deribit {e}")
            return None


async def get_deribit_btc_usd():
    url = "https://test.deribit.com/api/v2/public/get_index_price?index_name=btc_usd"
    return await get_deribit_crypto_price(url)


async def get_deribit_eth_usd():
    url = "https://test.deribit.com/api/v2/public/get_index_price?index_name=eth_usd"
    return await get_deribit_crypto_price(url)


if __name__ == "__main__":
    res = asyncio.run(get_deribit_btc_usd())
    res2 = asyncio.run(get_deribit_eth_usd())
    print(res)
    print(res2)
