# -*- coding -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config

engine = create_engine(
            Config['mysql-mysqldb'], encoding='utf-8',
            pool_recycle=600, pool_size=20, max_overflow=100,
            echo=False
            )

Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
