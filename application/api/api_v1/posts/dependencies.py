from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from application.core.models.db_helper import db_helper
from application.core.models.post import TgPost

from fastapi import Depends, HTTPException, Path, status


async def post_by_id(
        post_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.session_getter),
) -> TgPost:
    post = await crud.get_post(session=session, post_id=post_id)
    if post is not None:
        return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post {post_id} not found"
    )
