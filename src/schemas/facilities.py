from pydantic import BaseModel


class FacilitiesAdd(BaseModel):
    title: str


class Facility(BaseModel):
    id: int
    title: str
