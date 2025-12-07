from abc import ABCMeta

from sqlalchemy.orm import declarative_base, DeclarativeMeta


class DeclarativeABCMeta(DeclarativeMeta, ABCMeta):
    pass


class Base(declarative_base(metaclass=DeclarativeABCMeta)):
    __abstract__ = True
