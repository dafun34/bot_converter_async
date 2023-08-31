"""increase_user_int

Revision ID: ee9b231372dc
Revises: 7e7f587603a2
Create Date: 2023-08-31 07:34:09.917652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee9b231372dc'
down_revision = '7e7f587603a2'
branch_labels = None
depends_on = None


def upgrade():
    # Изменение типа столбца на BigInteger
    op.alter_column('users', 'id', type_=sa.BigInteger())


def downgrade():
    # Возвращение обратно к предыдущему типу столбца (если нужно)
    op.alter_column('users', 'id', type_=sa.Integer())
