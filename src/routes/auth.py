# src/routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user

# Importaciones de la aplicación y modelos
from app import db
from models.ModelUser import ModelUser
from models.entities.User import User

# Creación del Blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__)


# ===================================================
# === RUTA DE INICIO DE SESIÓN (LOGIN) ===
# ===================================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirigirlo a su página de inicio
    if current_user.is_authenticated:
        if current_user.role == 'Administrador':
            return redirect(url_for('admin.list_users'))
        return redirect(url_for('docente.home'))

    if request.method == 'POST':
        # Crear una entidad User temporal con los datos del formulario
        user_entity = User(id=0, username=request.form['username'], password=request.form['password'], role='')
        
        try:
            # Llamar al modelo para que verifique las credenciales
            logged_user = ModelUser.login(db, user_entity)
            
            if logged_user:
                # Si el modelo devuelve un usuario, iniciar la sesión con Flask-Login
                login_user(logged_user)
                flash(f'Bienvenido/a de nuevo, {logged_user.fullname or logged_user.username}!', 'success')
                # Redirigir según el rol del usuario
                if logged_user.role == 'Administrador':
                    return redirect(url_for('admin.list_users'))
                else:
                    return redirect(url_for('docente.home'))
            else:
                # Si el modelo devuelve None, las credenciales son incorrectas
                flash('Usuario o contraseña incorrectos. Por favor, inténtelo de nuevo.', 'danger')
                return render_template('auth/login.html')
        except Exception as ex:
            # Capturar cualquier error del sistema que el modelo pueda lanzar
            flash(str(ex), 'danger')
            return render_template('auth/login.html')
            
    # Si es una solicitud GET, simplemente mostrar la página de login
    return render_template('auth/login.html')


# ===================================================
# === RUTA DE CIERRE DE SESIÓN (LOGOUT) ===
# ===================================================
@auth_bp.route('/logout')
@login_required
def logout():
    """Cierra la sesión del usuario actual."""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))


# ===================================================
# === RUTA PARA CAMBIO DE CONTRASEÑA ===
# ===================================================
@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Permite al usuario autenticado cambiar su propia contraseña."""
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # 1. Verificar que la nueva contraseña y la confirmación coincidan
        if new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden.', 'warning')
            return redirect(url_for('auth.change_password'))

        # 2. Verificar que la contraseña actual sea correcta
        # Obtenemos el usuario completo desde la BD para acceder a su hash
        user_from_db = ModelUser.get_by_id(db, current_user.id)
        if not User.check_password(user_from_db.password, current_password):
            flash('La contraseña actual es incorrecta.', 'danger')
            return redirect(url_for('auth.change_password'))

        # 3. Verificar que la nueva contraseña sea segura
        is_strong, reason = ModelUser.is_password_strong(new_password)
        if not is_strong:
            flash(reason, 'warning')
            return redirect(url_for('auth.change_password'))

        # 4. Si todo es correcto, actualizar la contraseña en la BD
        try:
            ModelUser.update_password(db, current_user.id, new_password)
            flash('Tu contraseña ha sido actualizada exitosamente.', 'success')
            return redirect(url_for('docente.home')) # O a la página de perfil
        except Exception as ex:
            flash(str(ex), 'danger')
            return redirect(url_for('auth.change_password'))

    # Si es una solicitud GET, mostrar el formulario de cambio de contraseña
    return render_template('auth/change_password.html')


# ===================================================
# === RUTA PARA VALIDACIÓN DE CONTRASEÑA (AJAX) ===
# ===================================================
@auth_bp.route('/validate-password', methods=['POST'])
def validate_password():
    """
    Ruta llamada por JavaScript para validar la fortaleza de una contraseña en tiempo real.
    No requiere estar logueado, ya que se usa en el formulario de creación de usuario.
    """
    password = request.form.get('password', '')
    is_valid, reason = ModelUser.is_password_strong(password)
    
    # Preparamos una lista de razones si no es válida
    reasons = []
    if not is_valid:
        # Aquí puedes desglosar las razones si tu método 'is_password_strong' las devuelve
        # Por ahora, usamos el mensaje general.
        reasons.append(reason)
        
    return jsonify({'valid': is_valid, 'reasons': reasons})