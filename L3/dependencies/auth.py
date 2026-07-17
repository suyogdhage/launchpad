from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from config import settings
from datetime import datetime,timedelta,timezone
from dependencies.session import get_db
from fastapi import HTTPException,status,Depends


security=HTTPBearer()
pwd=CryptContext(schemes=["bcrypt"])

class Authentication:
    def hash_password(password:str):
        return pwd.hash(password)
    
    def verify_hash(password:str,hash):
        return pwd.verify(password,hash)
    
    def create_access_token(data):
        to_encode=data.copy()
        expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TIME_IN_MINUTES)
        to_encode.update({"exp":expire,"type":"access"})
        return jwt.encode(data,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    
    def decode_token(token=Depends(security),db=Depends(get_db)):
        try:
            data=jwt.decode(token.credentials,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
        return data
    

