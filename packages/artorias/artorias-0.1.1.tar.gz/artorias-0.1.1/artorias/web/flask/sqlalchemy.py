import functools

from sqlalchemy.orm import Mapped, mapped_column

from artorias.web.flask.exts import db


def transaction(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        else:
            return data

    return wrapper


class Model(db.Model):
    __abstract__ = True


class PkModel(Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    def get_by_id(cls, pk: int):
        return db.session.get(cls, pk)
