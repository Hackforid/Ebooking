# -*- coding -*-

#import umysqldb
#umysqldb.install_as_MySQLdb()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config

engine = create_engine(
            Config['mysql-connector'], encoding='utf-8', echo=False,
            pool_recycle=3600, pool_size=20,
#            strategy='threadlocal'
            )

Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
