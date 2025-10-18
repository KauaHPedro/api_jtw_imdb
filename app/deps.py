from fastapi import Query
from .config import settings

def pagination_params(
    page: int = Query(settings.PAGINATION_DEFAULT_PAGE, ge=1),
    page_size: int = Query(settings.PAGINATION_DEFAULT_SIZE, ge=1, le=settings.PAGINATION_MAX_SIZE),
):
    return {"page": page, "page_size": page_size}
