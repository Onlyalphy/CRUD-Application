from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USERNAME = "root"  
PASSWORD = "%4039295937Nrb%21" 
HOST = "127.0.0.1"
PORT = "3306"
DB_NAME = "ecommerce_db"     

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:%4039295937Nrb%21@127.0.0.1:3306/ecommerce_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
