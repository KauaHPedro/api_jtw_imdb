from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine
from .import_imdb import import_csv_if_empty
from .auth import router as auth_router
from .routers import movies as movies_router
from .routers import users as users_router
from .config import settings

app = FastAPI(
    title="IMDB API (Kaggle) com JWT",
    description="API segura (JWT) com dados do IMDB Top 1000 (Kaggle). CRUD + paginação + docs.",
    version="1.0.0",
    contact={"name": "Seu Nome", "url": "https://github.com/KauaHPedro"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)
import_csv_if_empty(limit=None)

app.include_router(auth_router)
app.include_router(movies_router.router)
app.include_router(users_router.router)

@app.get("/", tags=["Health"])
def root():
    return {"ok": True, "app": settings.APP_NAME}
