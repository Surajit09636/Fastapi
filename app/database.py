from time import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:suro1234@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# while True:  
#     try:
#         conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', password='suro1234', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected Successfully")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error:", error)
#         time.sleep(5)