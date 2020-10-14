from typing import Optional

from pydantic.main import BaseModel


class RedisData(BaseModel):
    key: str
    value: Optional[str] = None