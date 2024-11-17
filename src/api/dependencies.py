from fastapi import Depends, Query
from typing import Annotated
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(3, ge=1, le=10)]


PaginationDep = Annotated[PaginationParams, Depends()]
