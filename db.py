import atexit

from sqlalchemy import (
    ForeignKey, Text, Column, String, Integer, DateTime, create_engine, func)
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base


PG_DSN = 'postgresql://postgres:1@127.0.0.1:5432/flask_netology'

engine = create_engine(PG_DSN)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = Session.query_property()
atexit.register(engine.dispose)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    advertisements = relationship('Advertisement', backref='owner')


class Advertisement(Base):

    __tablename__ = 'advertisement'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(
        Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False
    )
    # owner = relationship('User', back_populates='advertisements')


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    # print(User.query.get(1))
