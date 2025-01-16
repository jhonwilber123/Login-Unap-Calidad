# src/config.py

class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Usuario root sin contraseña
    MYSQL_DB = 'unap_ccs_system'  # Cambiado a 'unap_ccs_system'

class ProductionConfig(Config):
    DEBUG = False
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'  # Usuario root sin contraseña
    MYSQL_DB = 'unap_ccs_system'  # Cambiado a 'unap_ccs_system'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig  # Agregado 'production'
}
