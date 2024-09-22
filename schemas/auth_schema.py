from pydantic import BaseModel

# Schema สำหรับรับข้อมูล JSON
class LoginRequest(BaseModel):
    username: str
    password: str