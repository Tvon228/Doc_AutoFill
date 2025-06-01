from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from src.backend.infrastructure.db.common.crud_repo import SqlAlchemyCrudRepo
from src.backend.core.auth.exceptions import LoginAlreadyInUseError
from src.backend.core.common.exceptions import AlreadyExistsError
from src.backend.infrastructure.db.users.model import UserModel
from src.backend.infrastructure.db.users.mappers import (
    map_user_model_to_entity,
    map_user_models_to_entities
)
from src.backend.core.users.repo import UsersRepositoryProtocol
from src.backend.core.users.entity import UserEntity
from src.backend.core.users.dto import AddUserDTO


class UsersRepository(UsersRepositoryProtocol):

    model = UserModel

    def __init__(self, session: AsyncSession, crud_repo: SqlAlchemyCrudRepo):
        self.session = session
        self.crud_repo: SqlAlchemyCrudRepo = crud_repo

    async def create(self, data: AddUserDTO, password_hash: str) -> UserEntity | None:
        try:
            user_model: UserModel = await self.crud_repo.create(
                name=data.name,
                role=data.role,
                password_hash=password_hash,
                email=data.email,
                phone=data.phone,
                added_by_user_id=data.added_by_user_id
            )
        except AlreadyExistsError:
            raise LoginAlreadyInUseError
        return map_user_model_to_entity(user_model)

    async def __get_user_by_params(self, **kwargs) -> UserEntity | None:
        user: UserModel = await self.crud_repo.get_one(**kwargs)
        return map_user_model_to_entity(user) if user else None

    async def get_by_id(self, ident: int) -> UserEntity | None:
        return await self.__get_user_by_params(id=ident)

    async def get_by_phone(self, phone: int) -> UserEntity | None:
        return await self.__get_user_by_params(phone=phone)

    async def get_by_email(self, email: str) -> UserEntity | None:
        return await self.__get_user_by_params(email=email)

    async def get_by_name(self, name: str) -> list[UserEntity] | None:
        result = await self.crud_repo.get_all(name=name)
        return map_user_models_to_entities(models=result)

    async def get_many(
            self,
            limit: int| None = None,
            offset: int | None = None,
            params: dict | None = None
    ) -> list[UserEntity]:
        if not params:
            params = {}

        result = await self.crud_repo.get_all(
            limit=limit,
            offset=offset,
            **params
        )
        return map_user_models_to_entities(models=result)

    async def update_one(self, user_id: int, values: dict) -> UserEntity:
        query = (
            update(self.model)
            .filter_by(id=user_id)
            .values(**values)
            .returning(self.model)
        )
        result = await self.session.execute(query)
        user: UserModel = result.scalar_one()
        return map_user_model_to_entity(user)

    async def delete(self, user_id: int) -> bool:
        user: UserModel | None = await self.session.get(ident=user_id, entity=self.model)
        if user:
            await self.session.delete(user)
            return True
        return False

