from sqlalchemy.orm import Session
from . import schemas
from pydantic import EmailStr
from datetime import datetime
from sun_stage import entity




def get_users_intern(db: Session):
    return db.query(entity.Intern).all()

def get_interns_by_services(service:str, db:Session):
    return db.query(entity.Intern).filter(entity.Intern.services == service).all()

def get_period(db:Session, period_start:datetime, period_end:datetime):
    return db.query(entity.Period).get((period_start, period_end))  #TODO: check

