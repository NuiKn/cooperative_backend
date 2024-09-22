from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "thar"  
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def check_permissions(request: Request):
    token = request.cookies.get("access_token") or request.headers.get("Authorization").split(" ")[1]
    
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
    except JWTError:
        raise HTTPException(status_code=403, detail="Not authenticated")

    request.state.role = role  # เก็บ role ไว้ใน request state
    return role

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("id")  # ดึง user_id ออกจาก payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
