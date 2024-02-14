from typing import Annotated
from fastapi import APIRouter
from starlette import status
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sun_stage.Intern.services import *
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from  sun_stage.auth import services, schemas
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sun_stage.config.database import SessionLocal

from sun_stage.auth.send_email_yt import send_dynamic_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTcwMTM3OTU0MCwiaWF0IjoxNzAxMzc5NTQwfQ.Yj4bN9w9cyQShTpLi6V1w-aHvKnS-opMEu08-49bl0s"
ALGORITHM = "HS256"

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=15)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

router = APIRouter()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = services.get_user_by_email(db=db, email=token_data.email)
    
    
    
    if user is None:
        raise credentials_exception
    return user



def get_current_administrator(current_user: schemas.UserCreate = Depends(get_current_user)):
    if not isinstance(current_user, Administrator):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an administrator",
        )
    return current_user

@router.post("/registeradmin")
async def register_admin(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    db_user = services.get_user_by_email(email= user.email, db=db)

  
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
    
    if len(user.password) < 5: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password too short")
   
    
    try:
        new_user = services.save_admin(db=db, user=user)
        # adding of sending of otp code by email
        ############################################
        try:
            otp = services.generate_and_save_otp(db=db, id_user=new_user.id, expiration_minutes=15)
            

            try:
               print("cocorico babe")
              
            #    await  send_email_async(email_to= new_user.email, subject="Activation Account", body={'fullname':new_user.fullname,'otpcode':otp.code, 'validtime': validtime})
               user_info = {'fullname':new_user.fullname,'otpcode':otp.code, 'validtime': 15, 'subject': 'Activation Account'}
               print("cocorico")
               send_dynamic_email(receiver_email=user.email, kwargs=user_info)

               return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Admin succesfully registred"})
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured when sending the mail")
            
        except Exception as e:
           raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Impossible to save otpcode")
            

        
        ##########################################
        #return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Admin succesfully registred"})
         
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    
    

@router.post("/active_account")
def active_account(form: schemas.UserActivate, db: Session = Depends(get_db)):
    
    user = services.get_user_by_email(email=form.email, db=db)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Account already activated")
    
    user_otp_valid = services.verify_otp(user_id=user.id, otp_code=form.otp, db=db)
    print("user otp is valid?", user_otp_valid) 
    if user_otp_valid ==False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Otp doesn't valid")

            
    try:
        services.activate_user(db=db, user_email=user.email)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Admin Account Successfully activated"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/login")
async def login_for_access_token(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = services.get_user_by_email(db, email=form_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not activated",
        )
    if not services.verify_password(password=form_data.password, db_password=user.password): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Générer le token ici
    access_token = create_jwt_token({"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/all")
async def get_all_admin(db:Session = Depends(get_db)):
    users = services.get_users_admin(db)
    return users

@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = services.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user



@router.post("/saveIntern")
async def save_intern(intern:schemas.InternCreate, current_user = Depends(get_current_administrator), db: Session = Depends(get_db)):
    
    db_user = services.get_user_by_email(intern.email)
    
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
    
    db_period = get_period(db=db, period_start=intern.period_start, period_end=intern.period_end)
    print('db_period', db_period)
    if db_period:
        period_id = db_period.id
    else:
        try:
            period_id = save_period(db=db, period_start=intern.period_start, period_end=intern.period_end).id
            
            try:
                user = save_intern(db=db, intern=intern)
                return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Intern succesfully registred"})
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        
        except Exception as e:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        
  