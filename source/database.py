from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from config import user,passwd,serverAddress,port, serverAddress_2, user_2,passwd_2,port_2

db_address=f"mssql+pymssql://{user}:{passwd}@{serverAddress}:{port}/User.db"

engine = create_engine(db_address)

if not database_exists(engine.url):
    create_database(engine.url)
    
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import source.DBMng

    Base.metadata.create_all(bind=engine)