from sqlalchemy.ext.declarative import declarative_base,Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Replace with your actual MySQL credentials
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PesonalInfo(Base):
    __tablename__ = "pesonal_info"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    gender = Column(String(255), index=True)
    hobbie = Column(String(255), index=True)