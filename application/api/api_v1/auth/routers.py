from application.api.dependencies.auth.backend import auth_backend
from fastapi import APIRouter

from application.core.schemas.users import UserRead, UserCreate
from application.core.config import settings

from ..users.dependencies import fastapi_users

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=['Auth']
)

# /login, /logout
router.include_router(
    router=fastapi_users.get_auth_router(auth_backend,),
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate,),
)
