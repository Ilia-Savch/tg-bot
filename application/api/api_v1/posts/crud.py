from sqlalchemy.ext.asyncio import AsyncSession
from application.core.models.post import TgPost
from application.core.schemas.posts import PostCreate, PostUpdatePartial
from datetime import datetime, timezone

async def get_post(session: AsyncSession, post_id: int) -> TgPost | None:
    return await session.get(TgPost, post_id)


async def create_post(session: AsyncSession, post_in: PostCreate) -> TgPost | None:
    data = post_in.model_dump()
    data['created_at'] = datetime.now(timezone.utc)
    post = TgPost(**data)
    session.add(post)
    await session.commit()
    await session.refresh(post) 
    return post


async def update_post(
        session: AsyncSession,
        post: TgPost,
        post_update: PostUpdatePartial,
        partial: bool = True) -> TgPost:
    for name, value in post_update.model_dump(exclude_unset=partial).items():
        setattr(post, name, value)
    await session.commit()
    await session.refresh(post)
    return post


async def delete_post(
    session: AsyncSession,
    post: TgPost
) -> None:
    await session.delete(post)
    await session.commit()
