from typing import TypeVar, Generic, Optional, Collection, Any, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Column
from sqlalchemy.exc import IntegrityError

from src.backend.infrastructure.db.common.base_model import BaseModel
from src.backend.core.common.exceptions import AlreadyExistsError


T = TypeVar("T", bound=BaseModel)

class SqlAlchemyCrudRepo(Generic[T]):

    def __init__(self, model: Type[T], session: AsyncSession):
        self.model: Type[T] = model
        self.session: AsyncSession = session

    async def create(self, **kwargs: Any) -> T:
        item = self.model(**kwargs)
        self.session.add(item)

        try:
            await self.session.flush()
            await self.session.refresh(item)
        except IntegrityError:
            raise AlreadyExistsError

        return item

    async def get_by_id(self, ident: int | str) -> Optional[T]:
        return await self.session.get(self.model, ident)

    async def get_one(self, **kwargs: Any) -> Optional[T]:
        result = await self.session.execute(select(self.model).filter_by(**kwargs))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[Column] = None,
        **kwargs: Any
    ) -> Collection[T]:
        query = select(self.model).filter_by(**kwargs)
        if order_by:
            query = query.order_by(order_by)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count(self, **kwargs) -> int:
        query = select(func.count()).select_from(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete(self, instance: T) -> None:
        await self.session.delete(instance)
        await self.session.flush()
