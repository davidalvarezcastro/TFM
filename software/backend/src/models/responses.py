from pydantic import BaseModel


class ErrorMessage(BaseModel):
    msg: str

class SuccessMessage(BaseModel):
    msg: str
