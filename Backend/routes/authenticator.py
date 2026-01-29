from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Schema.model import UserRole
from models.Authenticatior import LoginModel, RegisterModel
from Service.authenticationService import Authenticator
from db.db import get_db, User_DAO

router = APIRouter()

@router.post("/login")
def login(req: LoginModel, db: Session = Depends(get_db)):
    try:
        user = Authenticator.check_login(db, req.email, req.password)

        if not user:
            raise HTTPException(
                status_code=401, detail="Invalid email or password"
            )
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role.value,
            "is_verified_Advocate": user.is_verified_Advocate            
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/register")
def register(req: RegisterModel, db: Session = Depends(get_db)):
    try:
        
        if Authenticator.user_exists(db, req.email):
            raise HTTPException(
                status_code=400, detail="User already exists"
            )
        
        user = Authenticator.create_user(
            db, req.name, req.email, req.phone, req.password, area=req.region
        )
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role.value,
            "is_verified_Advocate": user.is_verified_Advocate
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print("REGISTER ERROR:", str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
