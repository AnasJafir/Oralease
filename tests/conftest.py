# tests/conftest.py
"""
Harnais de test OralEase : app Flask en SQLite mémoire, fixtures réutilisables.

app/utils/encryption.py lit ENCRYPTION_KEY *à l'import* (et lève si absente) :
on la pose donc AVANT d'importer quoi que ce soit de `app`.
"""
import os
import uuid
from datetime import date

from cryptography.fernet import Fernet

os.environ.setdefault("ENCRYPTION_KEY", Fernet.generate_key().decode())
os.environ.setdefault("SECRET_KEY", "test-secret")
# >= 32 octets : PyJWT avertit en dessous (RFC 7518 §3.2) pour HS256.
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key-for-the-suite-0123456789")

import pytest  # noqa: E402
from flask_jwt_extended import create_access_token  # noqa: E402

from app import create_app  # noqa: E402
from app.extensions import db as _db  # noqa: E402
from app.models import User, Patient  # noqa: E402
from config import Config  # noqa: E402


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # 'client_encoding' est spécifique à psycopg2 ; SQLite le refuse.
    SQLALCHEMY_ENGINE_OPTIONS = {}
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(app):
    """
    auth("doctor") -> en-têtes Bearer d'un utilisateur de ce rôle.

    Le token porte une identité *string* : Flask-JWT-Extended >= 4.7 rejette un
    `sub` entier en 422 avant la vue (souci pré-existant de /api/auth/login).
    On forge donc le token ici pour que les tests d'endpoint restent focalisés.
    """
    def _make(role="doctor"):
        uname = f"{role}_{uuid.uuid4().hex[:8]}"
        user = User(username=uname, email=f"{uname}@clinic.test", role=role)
        user.set_password("pw")
        _db.session.add(user)
        _db.session.commit()
        token = create_access_token(identity=str(user.id), additional_claims={"role": role})
        return {"Authorization": f"Bearer {token}"}
    return _make


@pytest.fixture
def patient(app):
    """Un patient valide (les RDV ont un patient_id en FK non nulle)."""
    p = Patient("Marie", "Curie", date(1980, 5, 12),
                "0600000000", "marie.curie@example.com", "RAS")
    _db.session.add(p)
    _db.session.commit()
    return p
