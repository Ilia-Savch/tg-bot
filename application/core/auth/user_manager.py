import logging

from typing import Optional, TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin

from application.core.models.user import User
from application.core.types.user_id import UserIdType


from core.config import settings

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):

    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(self, user: User, request: Optional["Request"] = None):
        log.info("User %r has registered.", user.id,)
