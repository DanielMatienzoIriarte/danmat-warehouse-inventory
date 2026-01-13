from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase

# model base class
class Base(DeclarativeBase, MappedAsDataclass):
    pass