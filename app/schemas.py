from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

# ========= AUTH =========

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)

# ========= MOVIES =========

class MovieBase(BaseModel):
    poster_link: Optional[str] = None
    series_title: Optional[str] = None
    released_year: Optional[int] = None
    certificate: Optional[str] = None
    runtime: Optional[str] = None
    genre: Optional[str] = None
    imdb_rating: Optional[float] = None
    overview: Optional[str] = None
    meta_score: Optional[int] = None
    director: Optional[str] = None
    star1: Optional[str] = None
    star2: Optional[str] = None
    star3: Optional[str] = None
    star4: Optional[str] = None
    no_of_votes: Optional[int] = None
    gross: Optional[str] = None

class MovieCreate(MovieBase):
    series_title: str = Field(..., min_length=1)

class MovieReplace(MovieBase):
    series_title: str = Field(..., min_length=1)

class MovieUpdate(MovieBase):
    pass

class MovieRead(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ========= PAGINAÇÃO =========

class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int

class PaginatedMovies(BaseModel):
    meta: PaginationMeta
    items: list[MovieRead]
