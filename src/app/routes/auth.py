from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.auth_service import AuthService
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

class OTPRequestModel(BaseModel):
    mobile: str
    purpose: str = "login"

class OTPVerifyModel(BaseModel):
    mobile: str
    otp: str
    purpose: str = "login"

@router.post("/send-otp")
def send_otp(
    req: OTPRequestModel,
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    # in dummy mode, we return the OTP
    otp = service.generate_otp(req.mobile, req.purpose)
    return {"message": "OTP sent successfully", "dummy_otp": otp} # remove dummy_otp in prod

@router.post("/verify-otp")
def verify_otp(
    req: OTPVerifyModel,
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    user = service.verify_otp(req.mobile, req.otp, req.purpose)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid OTP or expired")
    
    # Create token
    access_token = service.create_access_token(data={"sub": str(user.id), "role": user.role})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user.to_dict()
    }
