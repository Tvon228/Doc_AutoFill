from loguru import logger

from src.backend.core.auth.services.role_privilege import RolePrivilegeService
from src.backend.core.common.enums.user_roles import UserRoleEnum
from src.backend.core.common.interfaces.session import SessionProtocol
from src.backend.core.auth.interfaces import PasswordHasherProtocol
from src.backend.core.common.utils.dataclass_as_dict import iter_items
from src.backend.core.users.dto import AddUserDTO, UpdateUserDTO
from src.backend.core.users.exceptions import UserNotFoundError
from src.backend.core.users.repo import UsersRepositoryProtocol
from src.backend.core.users.entity import UserEntity


class UsersService:

    def __init__(self, users_repo: UsersRepositoryProtocol, session: SessionProtocol):
        self.users_repo: UsersRepositoryProtocol = users_repo
        self.session: SessionProtocol = session

    async def create_main_admin_if_not_exists(
            self,
            email: str,
            password: str,
            password_hasher: PasswordHasherProtocol,
    ) -> bool:
        """ Создаёт главного админа, если его нет """
        admin = await self.users_repo.get_by_email(email=email)
        if admin:
            return False

        data = AddUserDTO(
            name="MAIN ADMIN",
            email=email,
            password=password,
            role=UserRoleEnum.MAIN_ADMIN,
        )
        password_hash: str = password_hasher.hash(password)
        try:
            await self.users_repo.create(data=data, password_hash=password_hash)
        except Exception as e:
            logger.info(f"Main admin NOT created! {e}")
            return False
        else:
            logger.info("Main admin created!")
            return True

    async def create_user(
            self,
            requesting_user: UserEntity,
            new_user_data: AddUserDTO,
            password_hasher: PasswordHasherProtocol
    ) -> UserEntity:
        # Проверяем, есть ли права на создание
        RolePrivilegeService.can_create_user(requesting_user, new_user_data)

        # Создаём пользователя
        password_hash: str = password_hasher.hash(password=new_user_data.password)
        user = await self.users_repo.create(data=new_user_data, password_hash=password_hash)
        await self.session.commit()

        return user

    async def get_all(self) -> list[UserEntity]:
        return await self.users_repo.get_many()

    async def get_added_by_user(self, user_id: int) -> list[UserEntity]:
        params: dict = {"added_by_user_id": user_id}
        return await self.users_repo.get_many(params=params)

    async def update_user(
            self,
            user_id: int,
            requesting_user: UserEntity,
            update_data: UpdateUserDTO
    ) -> UserEntity:
        user: UserEntity = await self.users_repo.get_by_id(ident=user_id)
        if not user:
            raise UserNotFoundError

        RolePrivilegeService.can_edit_user(editor=requesting_user, target_user=user)

        non_empty_values: dict = {
            key: value
            for key, value in iter_items(update_data)
            if value is not None
        }

        updated_user: UserEntity = await self.users_repo.update_one(
            user_id=user_id,
            values=non_empty_values
        )
        await self.session.commit()
        return updated_user

    async def delete_user(
            self,
            requesting_user: UserEntity,
            delete_user_id: int,
    ) -> bool:
        delete_user: UserEntity = await self.users_repo.get_by_id(ident=delete_user_id)
        if not delete_user:
            raise UserNotFoundError
        RolePrivilegeService.can_delete_user(requesting_user=requesting_user, target_user=delete_user)
        is_deleted: bool = await self.users_repo.delete(user_id=delete_user_id)
        await self.session.commit()
        return is_deleted
