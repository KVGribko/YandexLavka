from pydantic import BaseModel


class BadRequestResponse(BaseModel):
    pass


class NotFoundResponse(BaseModel):
    pass
