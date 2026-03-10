from sqlalchemy.orm import Session
from database import PesonalInfo

def get_info(db: Session, item_id: int):
    return db.query(PesonalInfo).filter(PesonalInfo.id == item_id).first()

def create_info(db: Session, name: str, last_name: str, gender: str,hobbie:str):
    db_item = PesonalInfo(first_name=name, last_name=last_name, gender=gender,hobbie=hobbie)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item