from typing import Optional

from pydantic.main import BaseModel


class MongoData(BaseModel):
    name: str
    phone: Optional[str] = None
