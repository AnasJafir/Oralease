# app/__init__.py
from flask import Flask
from flask_cors import CORS
from config import DevelopmentConfig
from app.extensions import db, jwt, ma, migrate

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Activer CORS pour le front (dev + prod déployée sur Vercel)
    CORS(
        app,
        resources={r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "https://localhost:5173",
                # Frontend déployé (à adapter avec l'URL Vercel réelle)
                "https://oralease-frontend.vercel.app",
            ],
            "supports_credentials": False
        }}
    )

    # Initialisation des extensions
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # --- Enregistrement des APIs V2 (Backend complet) ---
    
    # 1. Authentification
    from app.apis.auth_api import auth_api_bp
    app.register_blueprint(auth_api_bp)

    # 2. Patients
    from app.apis.patients_api import patients_api_bp
    app.register_blueprint(patients_api_bp)

    # 3. Rendez-vous
    from app.apis.appointments_api import appointments_api_bp
    app.register_blueprint(appointments_api_bp)

    # 4. Inventaire
    from app.apis.inventory_api import inventory_api_bp
    app.register_blueprint(inventory_api_bp)

    # 5. Traitements & IA (Nouveau)
    from app.apis.treatments_api import treatment_api_bp
    app.register_blueprint(treatment_api_bp)

    from app.apis.xray_api import xray_api_bp
    app.register_blueprint(xray_api_bp)

    # 6. Dashboard
    from app.apis.dashboard_api import dashboard_api_bp
    app.register_blueprint(dashboard_api_bp)

    # 7. Facturation (Nouveau)
    from app.apis.invoices_api import invoices_api_bp
    app.register_blueprint(invoices_api_bp)
    
    @app.route('/status')
    def status():
        return {"status": "API V2 (Full Backend) Online", "db": "Connected"}

    return app