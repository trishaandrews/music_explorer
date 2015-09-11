from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

import settings

def db_connect():
    return create_engine(URL(**settings.params))

