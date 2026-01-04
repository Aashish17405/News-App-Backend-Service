import casbin
import casbin_sqlalchemy_adapter
from casbin_sqlalchemy_adapter import CasbinRule
from sqlalchemy.orm import Session
from ..database import engine
from ..config import settings
import os

_enforcer = None

def get_enforcer():
    global _enforcer
    if _enforcer is None:
        # Use the absolute path for the model file
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'rbac', 'rbac_model.conf')
        
        # Initialize the adapter
        adapter = casbin_sqlalchemy_adapter.Adapter(engine)
        
        # Initialize the enforcer
        _enforcer = casbin.Enforcer(model_path, adapter)
        
    return _enforcer

def init_rbac():
    """Ensure RBAC policies are set up or default roles exist."""
    # Ensure table exists
    CasbinRule.metadata.create_all(engine)
    
    e = get_enforcer()

    e.save_policy()

def add_policy_to_role(role: str, obj: str, action: str) -> bool:
    e = get_enforcer()
    res = e.add_policy(role, obj, action)
    e.save_policy()
    return res

def add_role_to_user(user_id: str, role: str) -> bool:
    e = get_enforcer()
    res = e.add_grouping_policy(user_id, role)
    e.save_policy()
    return res

def get_all_policies():
    e = get_enforcer()
    return e.get_policy()

def get_all_grouping_policies():
    e = get_enforcer()
    return e.get_grouping_policy()
