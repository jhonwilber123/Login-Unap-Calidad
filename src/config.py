# src/config.py

import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env que está en la raíz del proyecto
# La ruta busca el archivo .env un nivel por encima de donde está config.py
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class Config:
    """Configuración base, de la cual las demás heredarán."""
    
    # Clave secreta: la toma de la variable de entorno o usa una por defecto (menos segura).
    # Esto es crucial para la seguridad en producción.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-por-defecto-muy-dificil'
    
    # Desactivar el seguimiento de modificaciones de SQLAlchemy para ahorrar recursos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración para la carpeta de subida de archivos
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 Megabytes

class DevelopmentConfig(Config):
    """Configuración para el entorno de desarrollo."""
    
    # El modo DEBUG se controla con una variable de entorno.
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']
    
    # Configuración de la base de datos leída desde variables de entorno.
    MYSQL_HOST = os.environ.get('DB_HOST', 'localhost')
    MYSQL_USER = os.environ.get('DB_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('DB_PASSWORD', '')
    MYSQL_DB = os.environ.get('DB_NAME', 'unap_ccs_system')
    MYSQL_CURSORCLASS = 'DictCursor' # Muy útil para que las consultas devuelvan diccionarios

class ProductionConfig(Config):
    """Configuración para el entorno de producción."""
    
    DEBUG = False
    
    # En producción, NUNCA deberías tener valores por defecto.
    # La aplicación debería fallar si las variables no están definidas en el servidor.
    MYSQL_HOST = os.environ.get('DB_HOST')
    MYSQL_USER = os.environ.get('DB_USER')
    MYSQL_PASSWORD = os.environ.get('DB_PASSWORD')
    MYSQL_DB = os.environ.get('DB_NAME')
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # Podrías añadir más configuraciones de seguridad para producción aquí,
    # como configuraciones de logging, Sentry para reporte de errores, etc.


# Diccionario para acceder a las clases de configuración fácilmente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    # Podrías añadir una configuración para pruebas (testing)
    # 'testing': TestingConfig,

    'default': DevelopmentConfig
}