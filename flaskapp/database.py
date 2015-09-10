from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

import settings

url = "postgresql://%s:%s@%s/%s" %settings.params
#print url
engine = create_engine(url)#, convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

class Recs(Base):
    __table__ = Base.metadata.tables['recs']

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

