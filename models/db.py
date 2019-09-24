from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

import config

engine = create_engine(config.database_connection_string)
Session = scoped_session(sessionmaker(bind = engine))
Base = declarative_base()
