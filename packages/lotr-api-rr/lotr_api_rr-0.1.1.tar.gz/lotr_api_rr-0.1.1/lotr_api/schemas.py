from pydantic import BaseModel

from typing import TypeVar


class Movie(BaseModel):
    """Schema for a movie object."""
    _id: str
    academyAwardNominations: int
    academyAwardWins: int
    boxOfficeRevenueInMillions: float
    budgetInMillions: int
    name: str
    rottenTomatoesScore: float
    runtimeInMinutes: int


class Quote(BaseModel):
    """Schema for a quote object."""
    _id: str
    id: str
    dialog: str
    movie: str
    character: str


# Common type for API schema
SchemaType = TypeVar('SchemaType', type(Movie), type(Quote))