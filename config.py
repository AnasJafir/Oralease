# config.py
import os
from datetime import timedelta

class Config:
    """Configuration de base."""
    # Clé secrète pour Flask (Sessions, CSRF)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Configuration Base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'client_encoding': 'utf8'
    }
    
    # Configuration JWT (Authentification API)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Clé de chiffrement pour les données sensibles (HDS)
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

class DevelopmentConfig(Config):
    """Configuration pour le développement local."""
    DEBUG = True

class ProductionConfig(Config):
    """Configuration pour la production."""
    DEBUG = False
    # En prod, on force HTTPS pour les cookies
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
