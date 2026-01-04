from fastapi.testclient import TestClient
from src.app.main import app
from src.app.database import engine, get_db
from src.app.models import Base
from sqlalchemy.orm import Session
from src.app.models.user import User # Import needed to check DB

# Run this script with pytest
# pytest tests/test_auth_rbac.py

def test_auth_sync_flow():
    with TestClient(app) as client:
        # 1. Send OTP
        import random
        random_suffix = random.randint(1000, 9999)
        mobile = f"+91888888{random_suffix}"
        resp = client.post("/auth/send-otp", json={"mobile": mobile, "purpose": "login"})
        assert resp.status_code == 200
        data = resp.json()
        otp = data["dummy_otp"]
        
        # 2. Verify OTP (Creates user + Assigns default role in Casbin)
        verify_resp = client.post("/auth/verify-otp", json={"mobile": mobile, "otp": otp, "purpose": "login"})
        assert verify_resp.status_code == 200
        token = verify_resp.json()["access_token"]
        user_data = verify_resp.json()["user"]
        user_id = user_data["id"]
        
        # 2.5 Add 'read' policy for 'user' role (since default was removed)
        # Pass header
        headers = {"Authorization": f"Bearer {token}"}
        p_resp = client.post(
            "/api/v1/rbac/policies", 
            json={"role": "user", "obj": "news", "action": "read"},
            headers=headers
        )
        assert p_resp.status_code == 201 or p_resp.status_code == 200 # 200 if already exists
        
        # DEBUG: Check what policies exist
        debug_resp = client.get("/api/v1/rbac/policies", headers=headers)
        print(f"DEBUG POLICIES: {debug_resp.json()}")

        # 3. Verify Default Access (List News) - Requires (role='user', news, read)
        news_resp = client.get("/api/v1/news/", headers=headers)
        if news_resp.status_code != 200:
            print(f"DEBUG 403 RESPONSE: {news_resp.json()}")
        assert news_resp.status_code == 200
        
        # 4. Assign New Role (Admin) via API
        # We need to create a policy for 'admin' first to make it meaningful, 
        # or just assume 'admin' role exists conceptually.
        # Let's assign 'admin' role to this user.
        role_resp = client.post(
            "/api/v1/rbac/users/roles",
            json={"user_id": user_id, "role": "admin"},
            headers=headers
        )
        assert role_resp.status_code == 201
        
        # 5. Verify DB Sync
        # Check if the user's role in the DB is now "admin"
        # We need a new DB session or verify via API if there was a user-profile endpoint.
        # Since we have direct DB access in test:
        with Session(engine) as session:
            db_user = session.query(User).filter(User.id == user_id).first()
            assert db_user.role == "admin"
            print(f"DEBUG: User role in DB updated to: {db_user.role}")

        # 6. Verify Casbin Policy
        # List policies and check if 'admin' binding exists
        policy_resp = client.get("/api/v1/rbac/policies", headers=headers)
        grouping_policies = policy_resp.json()["grouping_policies"]
        # Expecting [user_id, "admin"]
        # Note: Casbin might store it as [uuid_str, "admin"]
        found = False
        for gp in grouping_policies:
            if gp[0] == user_id and gp[1] == "admin":
                found = True
                break
        assert found
