""" database model """
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

base_model = declarative_base()


# model 생성 예시

class App(base_model):
    """ example model """
    __tablename__ = 'app_token'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    access_token = Column(String(500))
    refresh_token = Column(String(50))
    iss = Column(String(50))
    cmp_id = Column(String(50))  # TODO 회사별로 하나니깐 아마도 유니크 체크 필요
    apps_id = Column(String(50))


class User(base_model): # TODO : app_id 또는 org_id 필요?
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    swit_id = Column(String(100))
    access_token = Column(String(500))
    refresh_token = Column(String(50))
