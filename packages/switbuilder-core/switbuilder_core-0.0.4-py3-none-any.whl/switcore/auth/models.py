from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

base_model = declarative_base()


class App(base_model):
    __tablename__ = 'app_token'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    access_token = Column(String(500))
    refresh_token = Column(String(50))
    iss = Column(String(50))
    cmp_id = Column(String(50), nullable=True)
    apps_id = Column(String(50))
