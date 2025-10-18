from fastapi import APIRouter, Depends
from ..auth import get_current_user
from ..schemas import UserRead

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserRead)
def read_me(current_user = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username}
