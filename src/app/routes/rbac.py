from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from ..dependencies import get_current_user
from ..models.user import User
from ..services import rbac_service
from ..database import get_db
from sqlalchemy.orm import Session

# NOTE: In production, you would add a permission check here!
# For example: dependencies=[Depends(PermissionChecker("rbac", "write"))]
# For now, we allow any authenticated user or specific simple check for testing.
router = APIRouter(prefix="/rbac", tags=["RBAC Management"])

class PolicyCreate(BaseModel):
    role: str
    obj: str
    action: str

class RoleAssignment(BaseModel):
    user_id: str
    role: str

@router.post("/policies", status_code=status.HTTP_201_CREATED)
def create_policy(policy: PolicyCreate, current_user: User = Depends(get_current_user)):
    # Simple check: only allow if user_role == 'admin' or something equivalent
    # For this dummy setup, we trust the caller if they are logged in.
    added = rbac_service.add_policy_to_role(policy.role, policy.obj, policy.action)
    if not added:
        return {"message": "Policy already exists"}
    return {"message": "Policy added successfully"}

@router.get("/policies")
def list_policies(current_user: User = Depends(get_current_user)):
    return {
        "policies": rbac_service.get_all_policies(),
        "grouping_policies": rbac_service.get_all_grouping_policies()
    }

@router.post("/users/roles", status_code=status.HTTP_201_CREATED)
def assign_role_to_user(
    assignment: RoleAssignment,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)  # Need DB access to update user table
):
    print(f"Assigning role(s) {assignment.role} to user {assignment.user_id}")
    roles = assignment.role if isinstance(assignment.role, list) else [assignment.role]
    added_any = False
    
    # Update Casbin
    for r in roles:
        added = rbac_service.add_role_to_user(assignment.user_id, r)
        added_any = added_any or bool(added)
    
    # Update User Table (Sync)
    # Note: If multiple roles are assigned, we might only be able to store one 'primary' role 
    # in the simple 'role' column of the User table unless we change the model.
    # For now, we take the last role in the list as the 'primary' display role.
    if roles:
        primary_role = roles[-1]
        user_to_update = db.query(User).filter(User.id == assignment.user_id).first()
        if user_to_update:
            user_to_update.role = primary_role
            db.commit()
            db.refresh(user_to_update)
            
    if not added_any:
        return {"message": "No new role assignments (they may already exist)"}
    return {"message": "Role(s) assigned successfully and user table updated"}