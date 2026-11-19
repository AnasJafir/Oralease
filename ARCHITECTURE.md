# Oralease – Architecture and Modularity

This document describes the current architecture of Oralease (Flask + SQLAlchemy + PostgreSQL) and proposes a modular target design to support scale and production-readiness.

---

## 1) Technology Stack

- Backend: Flask, SQLAlchemy, Flask-Migrate
- Database: PostgreSQL
- Auth: Session-based (decorators), planned JWT for APIs
- Frontend: Server-rendered Jinja templates (Bootstrap); future SPA optional
- Security: cryptography.Fernet for PHI encryption

---

## 2) Current Architecture Overview

At a high level, the app uses a monolithic Flask project with Blueprints grouping features. The application object and extensions are created in `app/__init__.py`, with Blueprints registered immediately and tables created at import time.

```
HTTP → Flask (app) → Blueprint route → View (db/session/access) → SQLAlchemy ORM → PostgreSQL
                                   ↘ (Jinja templates) / (JSON APIs)
```

### 2.1 Modules and Responsibilities

- `run.py`
  - Development entrypoint running `app` with debug server.

- `app/__init__.py`
  - Creates `Flask` app and `SQLAlchemy` instance.
  - Configures session cookie flags and database URI from env.
  - Registers Blueprints for web and API routes.
  - Calls `db.create_all()` at import time (okay for dev, replace with Alembic in prod).

- Blueprints (server-rendered UI):
  - `app/patients.py`, `app/appointment.py`, `app/inventory.py`, `app/treatment_plan.py`, `app/users.py`
  - Render Jinja templates in `templates/` and implement CRUD logic.

- API Blueprints (JSON):
  - `app/apis/patients_api.py`, `appointments_api.py`, `inventory_api.py`, `treatment_plan_api.py`, `users_api.py`
  - Expose REST-like endpoints, currently without schema validation.

- Data Layer:
  - `app/models.py`: `User`, `Patient` (encrypted PHI), `Appointment`, `InventoryItem`, `TreatmentPlan`, `DentalChart`.
  - Encryption helpers in `app/utils/encryption.py` using environment-provided Fernet key.

- Presentation:
  - `templates/` for Jinja views, `static/` for assets.

### 2.2 Cross-Cutting Concerns (Current)

- Auth: Session + role decorators in `app/authentication_decorators.py` and `app/users.py`.
- Config: Hard-coded in `app/__init__.py` with environment variables; no centralized config classes.
- Validation: Minimal; direct use of `request.form` in many endpoints.
- Error handling: Limited; try/except and global error handlers not uniform.
- Migrations: Alembic pinned in `requirements.txt`, but `db.create_all()` is used.

---

## 3) Data Model (Summary)

- `User(id, username, email, password_hash, role)`
- `Patient(id, first_name, last_name, date_of_birth, contact_number[encrypted], email[encrypted], medical_history[encrypted])`
- `Appointment(id, patient_id, appointment_date, notes)`
- `InventoryItem(id, name, description, quantity, threshold, unit)`
- `TreatmentPlan(id, patient_id, diagnosis, treatment_details, status)`
- `DentalChart(id, patient_id, tooth_data[JSON])`

Relationships are defined via SQLAlchemy relationships on `Appointment` and `TreatmentPlan` to `Patient`.

---

## 4) Request and Auth Flows

1. Client sends HTTP request.
2. Flask routes request to a Blueprint view.
3. Decorators enforce login/role checks using `session`.
4. View executes business logic, DB access via ORM, and returns JSON or renders a template.
5. For PHI fields, values are encrypted/decrypted at model boundaries.

Notes:
- APIs are protected by session-based decorators; migrating to JWT for API clients is advised.
- CSRF for form posts should be enabled via Flask-WTF in production.

---

## 5) Modularity Assessment (Current)

Pros:
- Clear feature grouping via Blueprints (patients, appointments, inventory, treatment).
- Single models module centralizes schema and encryption concerns.
- Utilities encapsulate encryption logic.

Gaps:
- App creation and extension init are not using the application factory pattern, making testing and configuration harder.
- Validation and error handling cross-cutting concerns are not centralized (schema validation, error mappers).
- `db.create_all()` at import time couples runtime with schema creation; replace with Alembic.
- No service layer or repository abstraction; views mix business logic and persistence.

---

## 6) Target Modular Architecture (Recommended)

Adopt a layered, testable architecture with clear boundaries and extension points.

```
Presentation (Blueprints/REST) ─┐
                               ├── Service Layer (domain logic, transactions)
External Integrations (storage) ┘          │
                                           ├── Repository Layer (ORM access, queries)
                                           └── Data Layer (SQLAlchemy models)

Cross-cutting: Config, Validation (Schemas), Auth/JWT, Logging, Errors, Caching, Rate Limiting
```

### 6.1 Application Factory & Config

- `app/__init__.py`
  - `db = SQLAlchemy()` (no app bound)
  - `migrate = Migrate()`
  - `csrf = CSRFProtect()`
  - `jwt = JWTManager()` (for API auth)
  - `limiter = Limiter()`
  - `def create_app(config_name): app = Flask(__name__); app.config.from_object(config[config_name]); init_app(app); register_blueprints(app); return app`

- `config.py`
  - `DevelopmentConfig`, `ProductionConfig` with secrets from env, pool settings, security headers, and file upload limits.

### 6.2 Services and Repositories

- `app/services/`
  - `patients_service.py`, `appointments_service.py`, `inventory_service.py`, `treatment_service.py`
  - Encapsulate business rules, transactions, and orchestration (e.g., creating appointments, checking inventory thresholds).

- `app/repositories/`
  - `patients_repo.py`, `appointments_repo.py`, etc., pure data access (queries, pagination, eager loading with `joinedload`).

- `app/schemas/`
  - Marshmallow schemas for input/output validation and serialization.

- `app/errors/`
  - Exception types and global error handlers mapping to JSON problem responses.

### 6.3 Cross-Cutting Enhancements

- Auth:
  - Sessions for web, JWT for APIs; role-based decorators consume claims.

- Validation:
  - Marshmallow on all API endpoints; reject malformed input early.

- Caching and Rate Limiting:
  - Redis for caching (e.g., patient lists, inventory snapshots), Flask-Limiter for per-IP/per-user limits.

- Logging/Observability:
  - Structured JSON logs, request IDs, error aggregation (Sentry), metrics (Prometheus).

- Migrations:
  - Alembic for schema changes; remove `db.create_all()` from runtime.

---

## 7) Folder Structure (Target)

```
app/
  __init__.py            # create_app, extension init
  config.py              # env-specific configs
  extensions.py          # db, migrate, jwt, csrf, limiter, cache
  models.py
  repositories/
  services/
  schemas/
  errors/
  apis/
    patients_api.py
    appointments_api.py
    inventory_api.py
    treatment_plan_api.py
    users_api.py
  web/
    patients.py
    appointment.py
    inventory.py
    treatment_plan.py
    users.py
templates/
static/
```

---

## 8) Evolution Plan

- Phase 1: Introduce `create_app`, move Blueprint registrations into factory, initialize extensions lazily.
- Phase 2: Add schemas, repositories, and services; migrate views to call services.
- Phase 3: Replace `db.create_all()` with Alembic; add indexes and connection pooling.
- Phase 4: Add JWT for APIs, CSRF for web forms, rate limits, caching, and structured logging.

---

## 9) Modularity Benefits

- Testability: Unit-test services and repositories without Flask app context.
- Scalability: Scale web and workers independently.
- Maintainability: Reduced coupling between view logic, persistence, and presentation.
- Security: Centralized validation, error handling, and auth hardening.
