# src/routes/admin.py (Versión Completa y Corregida)

from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from weasyprint import HTML

# Importa tus modelos y la instancia de la base de datos
from models.ModelUser import ModelUser
from models.ModelCV import ModelCV
# Asegúrate de que tu EditUserForm en forms.py tenga todos los campos necesarios
from forms import EditUserForm
from app import db, app

# Creamos el Blueprint para las rutas de administración
admin_bp = Blueprint('admin', __name__)

# ============================
# === GESTIÓN DE USUARIOS ===
# ============================

@admin_bp.route('/users')
@login_required
def list_users():
    """Muestra una lista de todos los usuarios del sistema."""
    if current_user.role != 'Administrador':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente.home'))
    
    try:
        users = ModelUser.get_all_users(db)
        return render_template('users/list_users.html', users=users)
    except Exception as ex:
        flash(f'Error al obtener la lista de usuarios: {ex}', 'danger')
        return redirect(url_for('docente.home'))

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    """Muestra el formulario y maneja la creación de un nuevo usuario."""
    if current_user.role != 'Administrador':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente.home'))

    if request.method == 'POST':
        # Leemos los datos del nuevo formulario separado
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        dni = request.form.get('dni')
        codigo = request.form.get('codigo')
        
        fullname_data = {
            'nombres': request.form['nombres'],
            'apellido_paterno': request.form['apellido_paterno'],
            'apellido_materno': request.form['apellido_materno']
        }
        
        try:
            # Llamamos al método del modelo refactorizado
            ModelUser.create_user(db, username, password, role, fullname_data, dni, codigo)
            flash('Usuario creado exitosamente.', 'success')
            return redirect(url_for('admin.list_users'))
        except Exception as ex:
            flash(str(ex), 'danger')
            return render_template('users/create_user.html')
    
    return render_template('users/create_user.html')

@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Muestra y procesa el formulario para editar un usuario existente."""
    if current_user.role != 'Administrador':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente.home'))
    
    try:
        # Usamos el nuevo método del modelo que obtiene los datos combinados
        user_data = ModelUser.get_user_with_details_by_id(db, user_id)
        if not user_data:
            flash('Usuario no encontrado.', 'warning')
            return redirect(url_for('admin.list_users'))

        # Pre-poblamos el formulario con los datos recuperados
        form = EditUserForm(data=user_data)

        if form.validate_on_submit():
            # La lógica de actualización ahora está centralizada en el modelo
            ModelUser.update_user_with_details(
                db, user_id, 
                form.username.data, 
                form.nombres.data, 
                form.apellido_paterno.data, 
                form.apellido_materno.data
            )

            # Si se proporcionó una nueva contraseña, la actualizamos por separado
            if form.password.data:
                is_strong, reason = ModelUser.is_password_strong(form.password.data)
                if not is_strong:
                    flash(reason, 'warning')
                    return render_template('users/edit_user.html', form=form, user=user_data)
                
                ModelUser.update_password(db, user_id, form.password.data)
            
            flash('Usuario actualizado correctamente.', 'success')
            return redirect(url_for('admin.list_users'))
        
        return render_template('users/edit_user.html', form=form, user=user_data)

    except Exception as ex:
        flash(f'Ocurrió un error al editar el usuario: {ex}', 'danger')
        return redirect(url_for('admin.list_users'))

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Elimina un usuario del sistema."""
    if current_user.role != 'Administrador':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente.home'))
    
    try:
        ModelUser.delete_user(db, user_id)
        flash('Usuario eliminado correctamente.', 'success')
    except Exception as ex:
        flash(f'Ocurrió un error al eliminar el usuario: {ex}', 'danger')
        
    return redirect(url_for('admin.list_users'))

# =============================
# === VISUALIZACIÓN DE REPORTES ===
# =============================

@admin_bp.route('/reports/personal_data', defaults={'page': 1})
@admin_bp.route('/reports/personal_data/page/<int:page>')
@login_required
def ver_datos_personal(page):
    """Muestra una lista paginada de todos los docentes."""
    if current_user.role != 'Administrador':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente.home'))

    try:
        # La lógica de paginación ahora vive en el modelo.
        resultados_por_pagina = 10
        paginated_data = ModelUser.get_paginated_docentes(db, page, resultados_por_pagina)
        
        return render_template('admin/ver_datos_personal.html', 
                               usuarios=paginated_data['usuarios'], 
                               page=page, 
                               total_paginas=paginated_data['total_paginas'])
    except Exception as ex:
        flash(f'Ocurrió un error al obtener los datos del personal: {ex}', 'danger')
        return redirect(url_for('docente.home'))

@admin_bp.route('/report/view_all/<int:user_id>')
@login_required
def view_all_data(user_id):
    """Muestra una página HTML con toda la información de un docente específico."""
    if current_user.role != 'Administrador':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente.home'))

    try:
        # Usamos el método del ModelCV que obtiene todos los datos
        datos_completos = ModelCV.get_cv_completo_por_usuario(db, user_id)
        
        if not datos_completos.get('datos_personales'):
             flash('No se encontraron datos para este usuario.', 'warning')
             return redirect(url_for('admin.ver_datos_personal'))

        return render_template('admin/view_all_data.html', datos=datos_completos)
    except Exception as ex:
        flash(f'Error al obtener los datos completos del docente: {ex}', 'danger')
        return redirect(url_for('admin.ver_datos_personal'))

@admin_bp.route('/report/generate_pdf/<int:user_id>')
@login_required
def generar_reporte_pdf(user_id):
    """Genera y descarga un reporte en PDF con toda la información de un docente."""
    if current_user.role != 'Administrador':
        flash('No tienes permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente.home'))

    try:
        # Reutilizamos el mismo método del modelo. ¡Principio DRY!
        datos_completos = ModelCV.get_cv_completo_por_usuario(db, user_id)
        
        if not datos_completos.get('datos_personales'):
             flash('No se pueden generar reportes para usuarios sin datos.', 'warning')
             return redirect(url_for('admin.ver_datos_personal'))

        # Renderizamos la plantilla HTML especial para PDF
        html_renderizado = render_template('pdf/reporte_template.html', 
                                           datos=datos_completos,
                                           base_url=request.host_url)

        # Usamos WeasyPrint para la conversión
        pdf = HTML(string=html_renderizado, base_url=request.host_url).write_pdf()

        # Creamos una respuesta de Flask para la descarga
        return Response(pdf,
                        mimetype='application/pdf',
                        headers={'Content-Disposition': f'attachment;filename=reporte_docente_{user_id}.pdf'})
    
    except Exception as ex:
        flash(f'Error al generar el reporte en PDF: {ex}', 'danger')
        return redirect(url_for('admin.ver_datos_personal'))