# src/app.py

from flask import Flask, redirect, url_for, render_template
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user

# Importar la configuración
from config import config

# Importar los modelos
from models.ModelUser import ModelUser

# Importar los Blueprints (nuestros controladores de rutas)
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.docente import docente_bp

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Inicialización de extensiones
csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'auth.login'  # Especifica la vista de login
login_manager_app.login_message = "Por favor, inicie sesión para acceder a esta página."
login_manager_app.login_message_category = "info"

# --- CONFIGURACIÓN DEL LOGIN MANAGER ---
@login_manager_app.user_loader
def load_user(id):
    """Carga el usuario desde la base de datos para la gestión de sesiones."""
    try:
        return ModelUser.get_by_id(db, id)
    except Exception as ex:
        # En caso de un error de base de datos durante la carga del usuario,
        # es mejor no propagar la excepción para evitar que la app se caiga.
        print(f"Error en user_loader: {ex}")
        return None

# --- RUTAS GLOBALES Y MANEJADORES DE ERRORES ---

@app.route('/')
def index():
    """Ruta principal que redirige al home si el usuario está autenticado, o al login si no lo está."""
    if current_user.is_authenticated:
        # Redirigir al home del docente o del admin según el rol
        if current_user.role == 'Administrador':
            return redirect(url_for('admin.list_users')) # O a un dashboard de admin
        else:
            return redirect(url_for('docente.home'))
    return redirect(url_for('auth.login'))

@app.errorhandler(404)
def page_not_found(error):
    """Manejador para errores 404 (Página no encontrada)."""
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """Manejador para errores 500 (Error interno del servidor)."""
    return render_template('error/500.html'), 500

@app.errorhandler(401)
def unauthorized(error):
    """Manejador para errores 401 (No autorizado)."""
    flash('No tienes permiso para acceder a esta página.', 'warning')
    return redirect(url_for('auth.login'))


# --- PUNTO DE ENTRADA DE LA APLICACIÓN ---

if __name__ == '__main__':
    # 1. Cargar la configuración desde el objeto 'development' en config.py
    app.config.from_object(config['development'])
    
    # 2. Inicializar la protección CSRF para la aplicación
    csrf.init_app(app)
    
    # 3. Registrar los Blueprints para organizar las rutas
    # El url_prefix añade un prefijo a todas las rutas dentro de ese blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(docente_bp, url_prefix='/docente')
    
    # 4. Registrar los manejadores de errores personalizados
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(401, unauthorized)
    
    # 5. Ejecutar la aplicación en modo de depuración
    app.run(debug=True)