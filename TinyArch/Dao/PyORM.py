#!/usr/bin/env python
# -*- coding:utf-8 -*-
import Config

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Dao import SqlAchemyOrm as Orm


class DbConnection:

    def __init__(self):
        self.__conn_str = Config.SQL_ALCHEMY_CONN_STR
        self.__max_overflow = Config.SQL_ALCHEMY_MAX_OVERFLOW
        self.conn = None

    def connect(self):
        engine = create_engine(self.__conn_str, max_overflow=self.__max_overflow)
        session = sessionmaker(bind=engine)
        self.conn = session()

        return self.conn

    def close(self):
        self.conn.commit()
        self.conn.close()


class NewsDao:

    def __init__(self):
        self.db_conn = DbConnection()

    def fetch_single_by_nid(self, nid):
        conn = self.db_conn.connect()
        result = conn.query(Orm.News).filter(Orm.News.nid == nid).first()
        self.db_conn.close()
        return result

    def fetch_all(self):
        conn = self.db_conn.connect()
        result = conn.query(Orm.News).all()
        self.db_conn.close()
        return result

    def fetch_all_join_type(self):
        conn = self.db_conn.connect()
        result = conn.query(Orm.News).join(Orm.NewsType, Orm.News.news_type_id == Orm.NewsType.nid, isouter=True).all()
        self.db_conn.close()
        return result


class UserInfoDao:

    def __init__(self):
        self.db_conn = DbConnection()

    def fetch_single_by_nid(self, nid):
        conn = self.db_conn.connect()
        result = conn.query(Orm.UserInfo).filter(Orm.UserInfo.nid == nid).first()
        self.db_conn.close()
        return result

    def fetch_single_by_user_pwd(self, user, pwd):
        conn = self.db_conn.connect()
        result = conn.query(Orm.UserInfo).filter(Orm.UserInfo.username == user,Orm.UserInfo.password == pwd ).first()
        self.db_conn.close()
        return result

    def fetch_all(self):
        conn = self.db_conn.connect()
        result = conn.query(Orm.UserInfo).all()
        self.db_conn.close()
        return result