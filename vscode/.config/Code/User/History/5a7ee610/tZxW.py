from typing import Union
from fastapi import FastAPI,Depends
from pydantic import BaseModel
import uvicorn
from crud import create_info
from sqlalchemy.orm import Session
from consts import DB_PASSWORD,DB_HOST,DB_INIT_DATABASE,DB_PORT,DB_TYPE
from database import SessionLocal,engine,Base

app = FastAPI()

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    gender: str
    hobbie: str

@app.post("/add_info")
async def add_info(data: PersonalInfo,db: Session = Depends(get_db)):

    create_info(data.first_name,data.last_name,data.gender,data.hobbie)

    return {"message": "Data received and printed", "data": data}

if __name__ == "__main__":
    uvicorn()