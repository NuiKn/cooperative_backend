from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from routers import auth_router, user__router
from routers.equipment_router import router as equipment_router
from routers.place_routers import router as place_router
from routers.placeEquipment_router import router as placeEquipment_router
# start thar
from routers.booking_router import router as booking_router   
from routers.returning_router import router as returning_router   
# end thar
from database import engine, Base

# สร้างฐานข้อมูล
Base.metadata.create_all(bind=engine)

app = FastAPI()

# กำหนด CORS (Cross-Origin Resource Sharing) ถ้าจำเป็น
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # เปลี่ยนเป็น URL ของคุณถ้าต้องการจำกัด
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ใช้ HTTPBearer สำหรับการส่ง Bearer Token
bearer_scheme = HTTPBearer()

# รวม router
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(user__router.router, prefix="/user", tags=["user"])
app.include_router(equipment_router, tags=["Equipment"])
app.include_router(place_router, tags=["Place"])
app.include_router(placeEquipment_router, tags=["PlaceEquipment"])

# start thar 
app.include_router(booking_router, tags=["Booking"])
app.include_router(returning_router, tags=["Returning"])
# end thar

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sports Equipment Rental System!"}


# Custom OpenAPI เพื่อรองรับ Bearer Token ใน Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sports Equipment Rental System API",
        version="1.0.0",
        description="API documentation for the Sports Equipment Rental System",
        routes=app.routes,
    )
    # เพิ่ม HTTPBearer Token ใน security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"  # หรือเปลี่ยนเป็นอะไรก็ได้ตามที่คุณใช้
        }
    }
    # เพิ่ม security ให้ API ทุกส่วนสามารถใช้ HTTPBearer ได้
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# กำหนดให้ app ใช้ custom OpenAPI schema
app.openapi = custom_openapi


