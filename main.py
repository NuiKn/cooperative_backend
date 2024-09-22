from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(user__router.router, prefix="/user", tags=["user"])




# รวม router
app.include_router(equipment_router,tags=["Equipment"])
app.include_router(place_router,tags=["Place"])
app.include_router(placeEquipment_router,tags=["PlaceEquipment"])


# start thar 
app.include_router(booking_router,tags=["Booking"])
app.include_router(returning_router,tags=["Returning"])
# end thar


@app.get("/")
def read_root():
    return {"message": "Welcome to the Sports Equipment Rental System!"}
