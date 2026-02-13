from backend.app.core.database import SessionLocal
from backend.app.users.models import User
from backend.app.core.security import hash_password

db = SessionLocal()

agent = User(
    email="agent@support.com",
    password_hash=hash_password("agent@123"),
    role="AGENT"
)

db.add(agent)
db.commit()
db.close()

print("Agent created successfully")
