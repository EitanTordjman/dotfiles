from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import create_engine,Column, Integer, String
from consts import DB_URL

engine = create_engine(DB_URL)
SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PesonalInfo(Base):
    __tablename__ = "pesonal_info"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    gender = Column(String(255), index=True)
    hobbie = Column(String(255), index=True)

