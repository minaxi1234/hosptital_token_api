import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import auth,admin
from app.api.v1.controllers.patient_token import router as patient_token_router
from app.api.v1.routes import websocket
from datetime import datetime
from app.db.session import SessionLocal
from app.db.seed_roles import seed_roles

from app.core.redis import test_redis_connection
from app.core.exceptions import (
    global_exception_handler,
    hospital_api_exception_handler, 
    http_exception_handler,
    validation_exception_handler,
    HospitalAPIException
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Hospital Token Management System")

@app.on_event("startup")
async def startup_event():
   test_redis_connection()
   db = SessionLocal()
   try:
       seed_roles(db)
   finally:
       db.close()
  
  

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
        "http://127.0.0.1:5173",],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HospitalAPIException, hospital_api_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# Include routers
app.include_router(auth.router)  # /auth endpoints
app.include_router(admin.router)
app.include_router(patient_token_router)  # /patients and /tokens endpoints
app.include_router(websocket.router)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)



    