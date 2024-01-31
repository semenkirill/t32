from pydantic import BaseModel


class LogCreate(BaseModel):
    user: str
    type: str
    message: str
