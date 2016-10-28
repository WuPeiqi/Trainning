#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy import ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

ENGINE = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/digchouti?charset=utf8", max_overflow=5)

Base = declarative_base()


class SendMsg(Base):
    __tablename__ = 'sendmsg'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(6))
    email = Column(String(32), index=True)
    times = Column(Integer, default=0)
    ctime = Column(TIMESTAMP)


class UserInfo(Base):
    __tablename__ = 'userinfo'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
    password = Column(String(32))
    email = Column(String(32))
    ctime = Column(TIMESTAMP)

    __table_args__ = (
        Index('ix_user_pwd', 'username', 'password'),
        Index('ix_email_pwd', 'email', 'password'),
    )

    def __repr__(self):
        return "%s-%s-%s" % (self.nid, self.username, self.email)


class NewsType(Base):
    __tablename__ = 'newstype'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    caption = Column(String(32))


class News(Base):
    __tablename__ = 'news'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    user_info_id = Column(Integer, ForeignKey("userinfo.nid"))
    news_type_id = Column(Integer, ForeignKey("newstype.nid"))
    ctime = Column(TIMESTAMP)
    title = Column(String(32))
    url = Column(String(128))
    content = Column(String(150))
    favor_count = Column(Integer, default=0)

    comment_count = Column(Integer, default=0)

    f = relationship('Favor', backref='n')


class Favor(Base):
    __tablename__ = 'favor'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    user_info_id = Column(Integer, ForeignKey("userinfo.nid"))
    news_id = Column(Integer, ForeignKey("news.nid"))
    ctime = Column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint('user_info_id', 'news_id', name='uix_uid_nid'),
    )


class Comment(Base):
    __tablename__ = 'comment'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    user_info_id = Column(Integer, ForeignKey("userinfo.nid"))
    news_id = Column(Integer, ForeignKey("news.nid"))
    reply_id = Column(Integer, ForeignKey("comment.nid"), nullable=True, default=None)
    up = Column(Integer)
    down = Column(Integer)
    ctime = Column(TIMESTAMP)
    device = Column(String(32))
    content = Column(String(150))


def init_db():
    Base.metadata.create_all(ENGINE)


def drop_db():
    Base.metadata.drop_all(ENGINE)


def session():
    cls = sessionmaker(bind=ENGINE)

    return cls()

    # drop_db()
    # init_db()