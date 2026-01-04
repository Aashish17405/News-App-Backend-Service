from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.auth import OTPRequest
from . import rbac_service
from ..config import settings
import random
import string
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def generate_otp(self, mobile_e164: str, purpose: str = "login") -> str:
        # Generate a 6-digit OTP
        otp = "".join(random.choices(string.digits, k=6))
        
        # Check if we should hash it. For now, we store plain or hashed? 
        # Ideally store hashed.
        otp_hash = pwd_context.hash(otp)
        
        # Expiration
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        
        otp_request = OTPRequest(
            mobile_e164=mobile_e164,
            otp_hash=otp_hash,
            purpose=purpose,
            expires_at=expires_at
        )
        self.db.add(otp_request)
        self.db.commit()
        
        # In a real app, send via SMS. Here we return it for the API response (Dummy)
        return otp

    def verify_otp(self, mobile_e164: str, otp: str, purpose: str = "login") -> Optional[User]:
        # Find valid OTP request
        # Order by issued_at desc to get latest
        otp_req = self.db.query(OTPRequest).filter(
            OTPRequest.mobile_e164 == mobile_e164,
            OTPRequest.purpose == purpose,
            OTPRequest.used == False,
            OTPRequest.expires_at > datetime.utcnow()
        ).order_by(OTPRequest.issued_at.desc()).first()
        
        if not otp_req:
            return None
            
        if not pwd_context.verify(otp, otp_req.otp_hash):
            return None
            
        # Mark used
        otp_req.used = True
        self.db.commit()
        
        # Get or Create User
        user = self.db.query(User).filter(User.mobile_e164 == mobile_e164).first()
        if not user:
            # Create a new user if not exists
            new_user = User( # Changed variable name to new_user
                mobile_e164=mobile_e164,
                username=f"user_{mobile_e164[-4:]}", # simple default username
                role="user", # Kept existing role assignment
                location_id=None # Default location # Added location_id
            )
            self.db.add(new_user) # Used self.db and new_user
            self.db.commit() # Used self.db
            self.db.refresh(new_user) # Used self.db and new_user
            
            # Explicitly assign default role (user) in Casbin
            # This ensures the 'g' policy (uuid, "user") is created
            rbac_service.add_role_to_user(str(new_user.id), "user") # Added RBAC call
            
            user = new_user # Assign new_user to user for consistent return
            
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt