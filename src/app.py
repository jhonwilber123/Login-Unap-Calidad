# src/app.py
from flask import Flask, redirect, url_for
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user

from config import config

# Models:
from models.ModelUser import ModelUser

# Blueprints (Rutas):
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.docente import docente_bp

# Inicialización de la App
app = Flask(__name__)

# Inicialización de extensiones
csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

# Configuración del Login Manager
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# Ruta principal que redirige al login si no está autenticado
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('docente.home')) # Nótese que ahora se usa el nombre del blueprint
    return redirect(url_for('auth.login'))

def page_not_found(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    # Cargar configuración
    app.config.from_object(config['development'])
    
    # Inicializar CSRF
    csrf.init_app(app)
    
    # Registrar Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(docente_bp, url_prefix='/docente') # Las rutas del docente estarán en /docente/home, etc.
    
    # Registrar manejador de errores
    app.register_error_handler(404, page_not_found)
    
    # Ejecutar la aplicación
    app.run()