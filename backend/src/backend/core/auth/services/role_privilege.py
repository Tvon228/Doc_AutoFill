from src.backend.core.auth.exceptions import PermissionDeniedError
from src.backend.core.common.enums.user_roles import UserRoleEnum
from src.backend.core.users.dto import AddUserDTO
from src.backend.core.users.entity import UserEntity


class RolePrivilegeService:

    _hierarchy: dict[UserRoleEnum, set[UserRoleEnum]] = {
        UserRoleEnum.MAIN_ADMIN: {UserRoleEnum.ADMIN, UserRoleEnum.EMPLOYEE, },
        UserRoleEnum.ADMIN: {UserRoleEnum.EMPLOYEE, },
        UserRoleEnum.EMPLOYEE: set(),
    }

    @classmethod
    def has_privilege(
            cls,
            user_role: UserRoleEnum,
            required_role: UserRoleEnum,
            *,
            exact_match: bool = False
    ) -> bool:
        """
        Проверяет, есть ли у пользователя требуемая привилегия
        Если exact_match = False, проверяет по иерархии
        """
        if exact_match:
            return user_role == required_role
        return (user_role == required_role) or (required_role in cls._hierarchy[user_role])

    @staticmethod
    def can_create_user(requesting_user: UserEntity, new_user_data: AddUserDTO):
        """
        Может ли пользователь добавить другого
        Raises:
            PermissionDeniedError - если нет прав
        """
        # Главного админа нельзя добавить
        if new_user_data.role == UserRoleEnum.MAIN_ADMIN:
            raise PermissionDeniedError("Cannot create user with 'MAIN_ADMIN' role")

        # Добавить админа может только главный админ
        if new_user_data.role == UserRoleEnum.ADMIN and requesting_user.role != UserRoleEnum.MAIN_ADMIN:
            raise PermissionDeniedError("Only MAIN_ADMIN can create ADMIN users")

    @staticmethod
    def can_edit_user(editor: UserEntity, target_user: UserEntity) -> None:
        """
        Может ли пользователь изменить данные другого пользователя
        Raises:
            PermissionDeniedError - если нет прав
        """
        if target_user.id == editor.id:  # Все пользователи могут менять свои данные
            return
        if editor.role == UserRoleEnum.MAIN_ADMIN:  # Главный админ может менять данные любого
            return
        if editor.role == UserRoleEnum.ADMIN:
            if target_user.added_by_user_id != editor.id:  # and target_user.id != editor.id
                raise PermissionDeniedError("ADMIN can't edit users they have not added")
            return

        # if editor.role == UserRoleEnum.EMPLOYEE:
        #     if target_user.id != editor.id:
        #         raise PermissionDeniedError("EMPLOYEE can only edit their own data")
        #     return True

        raise PermissionDeniedError("You don't have permission to edit this user")

    @classmethod
    def can_delete_user(cls, requesting_user: UserEntity, target_user: UserEntity) -> None:
        cls.can_edit_user(editor=requesting_user, target_user=target_user)
