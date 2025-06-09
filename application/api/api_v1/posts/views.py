from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models.post import TgPost
from application.core.schemas.posts import PostCreate, PostRead, PostUpdatePartial
from . import crud
from core.models.db_helper import db_helper
from .dependencies import post_by_id
from core.config import settings

router = APIRouter(tags=["Posts"], prefix=settings.api.v1.posts,)


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(post_in: PostCreate, session: AsyncSession = Depends(db_helper.session_getter),):
    return await crud.create_post(session=session, post_in=post_in)


@router.patch("/{post_id}/", response_model=PostRead)
async def update_post(
    post_update: PostUpdatePartial,
    post: TgPost = Depends(post_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.update_post(
        session=session,
        post=post,
        post_update=post_update,)


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: TgPost = Depends(post_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await crud.delete_post(post=post, session=session)
