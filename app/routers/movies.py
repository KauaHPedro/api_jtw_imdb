from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ..db import get_db
from ..models import Movie
from ..schemas import MovieCreate, MovieRead, MovieReplace, MovieUpdate, PaginatedMovies, PaginationMeta
from ..deps import pagination_params
from ..auth import get_current_user

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/", response_model=PaginatedMovies)
def list_movies(
    q: Optional[str] = None,
    pagination = Depends(pagination_params),
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    page = pagination["page"]; size = pagination["page_size"]

    query = db.query(Movie)
    if q:
        like = f"%{q}%"
        query = query.filter(Movie.series_title.ilike(like))

    total = query.count()
    items = query.order_by(Movie.id).offset((page - 1) * size).limit(size).all()

    total_pages = (total + size - 1) // size
    meta = PaginationMeta(page=page, page_size=size, total_items=total, total_pages=total_pages)

    items_read = [MovieRead.model_validate(i) for i in items]
    return {"meta": meta, "items": items_read}

@router.get("/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return MovieRead.model_validate(movie)

@router.post("/", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def create_movie(body: MovieCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    movie = Movie(**body.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return MovieRead.model_validate(movie)

@router.put("/{movie_id}", response_model=MovieRead)
def replace_movie(movie_id: int, body: MovieReplace, db: Session = Depends(get_db), user = Depends(get_current_user)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    for k, v in body.model_dump().items():
        setattr(movie, k, v)
    db.commit()
    db.refresh(movie)
    return MovieRead.model_validate(movie)

@router.patch("/{movie_id}", response_model=MovieRead)
def update_movie(movie_id: int, body: MovieUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(movie, k, v)
    db.commit()
    db.refresh(movie)
    return MovieRead.model_validate(movie)

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    db.delete(movie)
    db.commit()
    return None
