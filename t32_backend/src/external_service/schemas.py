from pydantic import BaseModel, Field


class LogCreate(BaseModel):
    user: str
    type: str
    message: str
