from pydantic import BaseModel


class IDBase(BaseModel):
    id: int
