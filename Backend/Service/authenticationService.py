from Schema.model import User, UserRole
from passlib.context import CryptContext
from datetime import datetime, timezone
from db.db import User_DAO
from sqlalchemy.orm import Session
import hashlib

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def normalize_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def hash_password(password: str) -> str:
    return pwd_context.hash(normalize_password(password))

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(normalize_password(password), hashed)

class Authenticator:

    @staticmethod
    def create_user(db: Session, name: str, email: str, phone: str, password: str, area: str = None):
        hashed_pwd = hash_password(password)

        user = User(
            name=name,
            email=email,
            phone=phone,
            password_hash=hashed_pwd,
            role=UserRole.Client,
            created_at = datetime.now(timezone.utc),
            is_verified_Advocate=False,
            area=area 
        )

        created_user = User_DAO.add_user(db, user)
                
        return created_user

    @staticmethod
    def user_exists(db: Session, email: str) -> bool:
        user = User_DAO.is_user_present(db=db, email=email)
        exists = user is not None
        return exists

    @staticmethod
    def check_login(db: Session, email: str, password: str):
        user = User_DAO.is_user_present(db=db, email=email)
        if not user:
            return False

        if verify_password(password, user.password_hash):
            return user
        
        return False
