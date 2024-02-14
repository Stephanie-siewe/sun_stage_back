from pydantic import EmailStr
from sqlalchemy.orm import Session
from . import schemas
from sun_stage import entity
from passlib.context import CryptContext
import random
import datetime



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str):
   return pwd_context.hash(password)

def save_admin(db:Session, user: schemas.UserCreate):
    
    
    hashed_password = get_password_hash(user.password)
    print('hashed password is ', hashed_password)
    
    db_user = entity.Administrator(
        fullname=user.fullname,
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password,
        created_by=user.email,
        updated_by=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def generate_and_save_otp(db:Session, id_user:int, expiration_minutes:int): 
    otp = str(random.randint(100000, 999999))
    print(f"OTP code for user {id_user}: {otp}")
    
    expiration_time_ = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    print("expiration date",expiration_time_)
    otp_instance = entity.Otpcode(user_id=id_user, code=otp, expiration_time=expiration_time_)
    print("JellyMerry")
    db.add(otp_instance)
    db.commit()
    db.refresh(otp_instance)
    return otp_instance



def verify_otp(user_id: int, otp_code: str, db: Session):
  
    otp_instance = db.query(entity.Otpcode).filter_by(user_id=user_id, code=otp_code).first()
    print('otp_instance', otp_instance.expiration_time)


    if otp_instance and datetime.datetime.utcnow() <= otp_instance.expiration_time:
        return True
    else:
        return False

def activate_user(user_email:str, db: Session):
    db_user = get_user_by_email(db=db, email=user_email)
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    print("Successfully Activated")
    
    


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(entity.User).filter(entity.User.email == email).first()

def get_user_by_id(db:Session,user_id:int):
    return db.query(entity.User).filter(entity.User.id==user_id).first()


def verify_password(password:str, db_password:str):
      return pwd_context.verify(password, db_password)
  
def get_users_admin(db: Session):
    return db.query(entity.Administrator).all()












def save_intern(db: Session, intern: schemas.InternCreate,created_by: EmailStr):
    
    hashed_password = get_password_hash(intern.password)
    print('hashed password is ', hashed_password)
    
    db_user = entity.Intern(
        email = intern.email,
        phone_number = intern.phone_number, 
        services = intern.service,
        fullname = intern.fullname,
        created_by = created_by,
        updated_by = created_by
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
def save_period(db:Session, period_start:datetime.datetime, period_end:datetime.datetime):
    
    db_period = entity.Period(
        start_date = period_start,
        end_date = period_end
    )
    
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    
    return db_period

    

