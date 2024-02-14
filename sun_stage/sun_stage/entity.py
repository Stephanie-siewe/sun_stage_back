from .config.database import Base 
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, BOOLEAN, Integer,ForeignKey, String, Enum, DateTime





class ServicesEnterprise(Enum):
    """ services of enterprise """
    Marketing = "Marketing"
    Development = "Development"



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(BOOLEAN, default=False)
    phone_number = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow) 
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    profile_image_url = Column(String, default=None)
    created_by = Column(String, default=None)
    updated_by = Column(String, default=None)
    is_deleted = Column(BOOLEAN, default=False)
    type = Column(String)
   
    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity" : "user"
    }
    
    
class Administrator(User):
    __tablename__ = 'administrators'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    
    __mapper_args__ = {
        
        "polymorphic_identity" : "administrator",
        'inherit_condition': (id == User.id)
        
    }
    
class Intern(User):
    __tablename__ = 'interns'
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    services = Column(String)
    period_id = Column(ForeignKey("periods.id"))
    period = relationship("Period")
    
    __mapper_args__ = {
        
        "polymorphic_identity" : "intern",
        'inherit_condition': (id == User.id)
    }


class Period(Base):
    __tablename__ = 'periods'
    id = Column(Integer, primary_key = True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    
class Otpcode(Base):
    __tablename__ = 'otps'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    code = Column(String)
    expiration_time = Column(DateTime)

    # def __init__(self, user_id, code, expiration_minutes):
    #     self.user_id = user_id
    #     self.code = code
    #     self.expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)