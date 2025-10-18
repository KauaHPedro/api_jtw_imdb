from pathlib import Path
import pandas as pd
from .db import engine, Base, SessionLocal
from .models import Movie
from .config import settings

CSV_PATH = Path(settings.DATASET_PATH)

EXPECTED = [
    "Poster_Link","Series_Title","Released_Year","Certificate","Runtime","Genre",
    "IMDB_Rating","Overview","Meta_score","Director",
    "Star1","Star2","Star3","Star4","No_of_Votes","Gross",
]

def _to_int(x):
    try:
        return int(str(x).strip())
    except:
        return None

def _to_float(x):
    try:
        return float(str(x).strip())
    except:
        return None

def import_csv_if_empty(limit: int | None = None):

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        if db.query(Movie).first():
            print("[IMDB] movies já populada. Pulando import.")
            return

    if not CSV_PATH.exists():
        print(f"[IMDB] CSV não encontrado em {CSV_PATH}. Pulando import.")
        return

    df = pd.read_csv(CSV_PATH)

    cols = list(df.columns)
    if cols != EXPECTED:
        raise ValueError(
            "Colunas do CSV não batem com o esperado.\n"
            f"Esperado ({len(EXPECTED)}): {EXPECTED}\n"
            f"Encontrado ({len(cols)}): {cols}"
        )

    df["Released_Year"] = df["Released_Year"].apply(_to_int)
    df["IMDB_Rating"]   = df["IMDB_Rating"].apply(_to_float)
    df["Meta_score"]    = df["Meta_score"].apply(_to_int)
    df["No_of_Votes"]   = df["No_of_Votes"].apply(lambda v: _to_int(str(v).replace(",", "")))

    if limit:
        df = df.head(limit)

    records = df.to_dict(orient="records")

    inserted = 0
    with SessionLocal() as db:
        for r in records:
            movie = Movie(
                poster_link  = r["Poster_Link"],
                series_title = r["Series_Title"],
                released_year= r["Released_Year"],
                certificate  = r["Certificate"],
                runtime      = r["Runtime"],
                genre        = r["Genre"],
                imdb_rating  = r["IMDB_Rating"],
                overview     = r["Overview"],
                meta_score   = r["Meta_score"],
                director     = r["Director"],
                star1        = r["Star1"],
                star2        = r["Star2"],
                star3        = r["Star3"],
                star4        = r["Star4"],
                no_of_votes  = r["No_of_Votes"],
                gross        = r["Gross"],
            )
            db.add(movie)
            inserted += 1
        db.commit()

    print(f"[IMDB] Import concluído: {inserted} registros inseridos.")
