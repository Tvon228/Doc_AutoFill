"""fix templates table

Revision ID: bcbe232803b0
Revises: 3e3bb89f5793
Create Date: 2025-05-20 23:04:32.310657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcbe232803b0'
down_revision: Union[str, None] = '3e3bb89f5793'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


field_type_enum = sa.Enum('SCALAR', 'OBJ_ATTR', name='fieldtypeenum')


def upgrade() -> None:
    """Upgrade schema."""
    field_type_enum = sa.Enum('SCALAR', 'OBJ_ATTR', name='fieldtypeenum')
    field_type_enum.create(op.get_bind())  # создаём enum в БД

    op.add_column('template_fields', sa.Column('field_type', field_type_enum, nullable=False))
    op.create_unique_constraint(None, 'template_fields', ['id'])
    op.create_unique_constraint(None, 'templates', ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'templates', type_='unique')
    op.drop_constraint(None, 'template_fields', type_='unique')
    op.drop_column('template_fields', 'field_type')

    field_type_enum = sa.Enum('SCALAR', 'OBJ_ATTR', name='fieldtypeenum')
    field_type_enum.drop(op.get_bind())  # удаляем enum из БД