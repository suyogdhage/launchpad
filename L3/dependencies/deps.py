from fastapi import Depends,HTTPException
from dependencies.auth import security
from config import settings
from jose import jwt

async def get_current_user(token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials,settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def role_checker(role):
    async def checker(user=Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return checker

def access(roles:list[str]):
    async def checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return checker