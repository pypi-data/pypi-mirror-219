import sqlalchemy.types as types
import sqlalchemy.dialects.postgresql as sa_pg
from sqlalchemy_utils import Ltree as PGLtree

__all__ = ['CITEXT', 'Ltree']


class CITEXT(types.UserDefinedType, sa_pg.TEXT):
    """Postgres case-insensitive text data type."""

    def get_col_spec(self):  # noqa: required
        return 'CITEXT'


class Ltree(PGLtree):
    """Postgresql Ltree data type."""

    @classmethod
    def validate(cls, path):
        pass
