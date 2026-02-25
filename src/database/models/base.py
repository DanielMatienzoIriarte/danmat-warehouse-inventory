from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


# model base class
class Base(DeclarativeBase, MappedAsDataclass):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    __mapper_args__ = {"eager_defaults": True}
