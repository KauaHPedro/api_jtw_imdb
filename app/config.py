from pydantic import BaseModel
import os
from datetime import timedelta
from pydantic import BaseModel
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    APP_NAME: str = "IMDB API (Kaggle) com JWT"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    ALGORITHM: str = "HS256"
    DB_URL: str = os.getenv("DB_URL")
    DATASET_PATH: str = os.getenv("DATASET_PATH")

    PAGINATION_DEFAULT_PAGE: int = 1
    PAGINATION_DEFAULT_SIZE: int = 10
    PAGINATION_MAX_SIZE: int = 100

    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

settings = Settings()