from pydantic import BaseModel


class DogWalkerBase(BaseModel):
    name: str
    phone_number: str


class DogWalkerRead(DogWalkerBase):
    pass
