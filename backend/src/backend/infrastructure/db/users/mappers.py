from typing import Collection

from src.backend.core.users.entity import UserEntity, UserId
from src.backend.infrastructure.db.users.model import UserModel


def map_user_model_to_entity(model: UserModel) -> UserEntity:
    return UserEntity(
        id=UserId(model.id),
        added_by_user_id=UserId(model.added_by_user_id),
        name=model.name,
        role=model.role,
        password_hash=model.password_hash,
        registered_at=model.registered_at,
        email=model.email,
        phone=model.phone,
        photo=None
    )


def map_user_models_to_entities(models: Collection[UserModel]) -> list[UserEntity]:
    return [
        map_user_model_to_entity(model=model)
        for model in models
    ]
