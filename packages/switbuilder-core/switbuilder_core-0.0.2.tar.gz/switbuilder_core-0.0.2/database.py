""" google cloud sql 연결 """
import pymysql
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy.orm import sessionmaker, Session

from auth import models
from config import settings


def connect_sql() -> sqlalchemy.engine.base.Engine:
    """ connect sql with env operation """

    if settings.ENV_OPERATION == "local":
        return connect_tcp_socket_local()

    return connect_with_connector()


def connect_tcp_socket_local() -> sqlalchemy.engine.base.Engine:
    """ local mysql server 에서 sqlalchemy engine 가져오기 """
    db_host = settings.DB_HOST
    db_port = settings.DB_PORT
    db_user = settings.DB_USERNAME
    db_pass = settings.DB_PASSWORD
    db_name = settings.DB_NAME

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name
        ),

        # [START_EXCLUDE]
        # Pool size is the maximum number of permanent connections to keep.
        pool_size=10,

        # Temporarily exceeds the set pool_size if no connections are available.
        max_overflow=10,

        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.

        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        pool_timeout=30,  # 30 seconds

        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # re-established
        pool_recycle=1800,  # 30 minutes
        # [END_EXCLUDE]
    )
    return pool


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """ google cloud sql 에 연결된 sqlalchemy engine 가져오기 """
    instance_connection_name = settings.DB_CONNECTION_NAME
    db_user = settings.DB_USERNAME
    db_pass = settings.DB_PASSWORD
    db_name = settings.DB_NAME

    ip_type = IPTypes.PRIVATE if settings.PRIVATE_IP else IPTypes.PUBLIC

    connector = Connector(ip_type)

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
        # [START_EXCLUDE]
        # Pool size is the maximum number of permanent connections to keep.
        pool_size=30,

        # Temporarily exceeds the set pool_size if no connections are available.
        max_overflow=30,

        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.

        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        pool_timeout=30,  # 30 seconds

        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # re-established
        pool_recycle=1800,  # 30 minutes
        # [END_EXCLUDE]
    )
    return pool


def get_db_session() -> Session:
    db_session = sessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


engine = connect_sql()
models.base_model.metadata.create_all(engine)
sessionLocal = sessionmaker(engine)
