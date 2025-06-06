"""add template models

Revision ID: 3e3bb89f5793
Revises: 0643d9dba546
Create Date: 2025-05-19 15:47:18.700426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e3bb89f5793'
down_revision: Union[str, None] = '0643d9dba546'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

field_data_type_enum = sa.Enum('NUMBER', 'TEXT', 'DATE', 'OBJECT_ATTRIBUTE', name='fielddatatypeenum')

def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('templates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('file_name', sa.String(length=100), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )
    op.create_table('template_fields',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('data_type', field_data_type_enum, nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('name', 'template_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('template_fields')
    op.drop_table('templates')
    field_data_type_enum.drop(op.get_bind())
    # ### end Alembic commands ###
