from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .database import get_db
from .services.rbac_service import get_enforcer
from .config import settings
from .models.user import User

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

class PermissionChecker:
    def __init__(self, action: str = "read", obj: str = "data"):
        self.action = action
        self.obj = obj

    async def __call__(self, user: User = Depends(get_current_user)):
        enforcer = get_enforcer()
        # Check permission: sub, obj, act
        # We pass user.id (as string) as the subject. Casbin will look up roles via 'g' policies.
        # e.g. g(user_id, "admin") && p("admin", "news", "delete")
        if not enforcer.enforce(str(user.id), self.obj, self.action):
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return True