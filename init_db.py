"""
Script d'initialisation de la base de données.
Crée toutes les tables et un utilisateur admin par défaut.
"""

from app import create_app
from app.extensions import db
from app.models import User

def init_db():
    """Initialise la base de données."""
    app = create_app()
    
    with app.app_context():
        # Reset complet (DEV ONLY)
        print("⚠ SUPPRESSION DE TOUTES LES TABLES (DEV MODE)...")
        # Tweaking to drop unknown tables (ghosts)
        try:
            with db.engine.connect() as conn:
                conn.execute(db.text("DROP TABLE IF EXISTS treatment_suggestions CASCADE"))
                conn.execute(db.text("DROP TABLE IF EXISTS medical_records CASCADE")) # Just in case
                conn.commit()
        except Exception as e:
            print(f"Warning during pre-cleanup: {e}")

        db.drop_all()
        print("✓ Tables supprimées.")

        # Créer toutes les tables
        print("Création des tables...")
        db.create_all()
        print("✓ Tables créées avec succès!")
        
        # Vérifier si un admin existe déjà
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            # Créer un utilisateur admin par défaut
            print("\nCréation de l'utilisateur admin par défaut...")
            admin = User(
                username='admin',
                email='admin@oralease.com',
                role='admin'
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("✓ Utilisateur admin créé!")
            print("  - Username: admin")
            print("  - Password: admin123")
            print("  - Email: admin@oralease.com")
        else:
            print("\n⚠ Un utilisateur admin existe déjà.")
        
        # Créer un utilisateur standard pour les tests
        user = User.query.filter_by(username='user').first()
        
        if not user:
            print("\nCréation d'un utilisateur standard pour les tests...")
            user = User(
                username='user',
                email='user@oralease.com',
                role='user'
            )
            user.set_password('user123')
            
            db.session.add(user)
            db.session.commit()
            
            print("✓ Utilisateur standard créé!")
            print("  - Username: user")
            print("  - Password: user123")
            print("  - Email: user@oralease.com")
        else:
            print("\n⚠ Un utilisateur standard existe déjà.")
        
        print("\n" + "="*50)
        print("Base de données initialisée avec succès!")
        print("="*50)
        print("\nVous pouvez maintenant démarrer l'application avec:")
        print("  flask run")
        print("\nPuis tester l'API avec Postman en vous connectant:")
        print("  POST http://localhost:5000/api/auth/login")
        print("  Body: {\"username\": \"admin\", \"password\": \"admin123\"}")

if __name__ == '__main__':
    init_db()
