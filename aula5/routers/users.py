from fastapi import APIRouter, Depends
from routers.auth import get_current_user
from models.user import User

router = APIRouter()

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
