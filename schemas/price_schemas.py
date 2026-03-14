import time
import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PriceCreate(BaseModel):
    ticker: Literal["btc", "eth"] = Field(
        description="Name of the crypto", examples=["btc", "eth"]
    )


class PriceRead(PriceCreate):
    id: uuid.UUID = Field(description="Unique id of the price")
    price: float = Field(description="Price for the ticker in usd")
    timestamp: float = Field(
        description="Timestamp, made with time.time()", default=time.time()
    )
    model_config = ConfigDict(from_attributes=True)
