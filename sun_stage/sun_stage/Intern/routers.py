from starlette import status
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sun_stage.config.database import SessionLocal
from  sun_stage.Intern import services,schemas
from sun_stage.auth.services import get_user_by_email
from sun_stage.auth.routers import get_current_administrator


router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
@router.get("/getAllIntern")
async def get_all_interns(db: Session = Depends(get_db)):
    return services.get_users_intern(db=db)


@router.get("/getByService/{service}")
async def get_interns_by_services(service:str, db: Session = Depends(get_db)):
    return get_interns_by_services(service=service, db=db)


  
    
    
    
        