from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

vals = {}
#(username, password, host, database)
with open("params.csv", 'r') as pf:
    for line in pf:
        kvs = line.strip().split(",")
        vals[kvs[0]] = kvs[1]       
params = (vals["user"], vals["password"], vals["host"], vals["database"])

url = "postgresql://%s:%s@%s/%s" %params
#print url
engine = create_engine(url)#, convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

class Recs(Base):
    __table__ = Base.metadata.tables['recs']

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

