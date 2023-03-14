"""Модуль создания модели валют."""
import sqlalchemy as sa

from tables.base import Base


class Currency(Base):
    """Модель валют."""

    __tablename__ = "currencies"

    id = sa.Column(
        "id", sa.Integer, primary_key=True, index=True, autoincrement=True
    )
    source_id = sa.Column(
        "source_id", sa.String(14), unique=False, nullable=False
    )
    name = sa.Column("name", sa.String(200), nullable=True)
    char_code = sa.Column("char_code", sa.String(200), nullable=True)
    value = sa.Column(sa.DECIMAL(precision=10, scale=2), nullable=True)
    is_active = sa.Column(sa.Boolean, default=True)
    updated_at = sa.Column(sa.DateTime)
    ordering_id = sa.Column(sa.Integer(), nullable=True)
