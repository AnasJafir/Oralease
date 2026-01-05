from app import create_app
from app.models import User
from app.extensions import db

app = create_app()
with app.app_context():
    users = User.query.all()
    print(f"Users found: {len(users)}")
    for u in users:
        print(f"User: {u.username}, Role: {u.role}")
        if u.username == 'admin':
            print(f"Check 'admin123': {u.check_password('admin123')}")
