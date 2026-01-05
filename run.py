# run.py
from app import create_app

# Création de l'instance de l'application via la factory
app = create_app()

if __name__ == '__main__':
    # Lancement du serveur de développement
    app.run(debug=True, port=5000)