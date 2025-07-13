# src/routes/docente.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import login_required, current_user
import os
import time
from werkzeug.utils import secure_filename
import logging

# Importaciones de la aplicación y modelos
from app import db, app
from models.ModelCV import ModelCV
# Importar TODOS los formularios de tu archivo forms.py
from forms import *

# Creación del Blueprint para todas las rutas del docente
docente_bp = Blueprint('docente', __name__)

# --- FUNCIÓN DE UTILIDAD PARA GUARDAR ARCHIVOS ---
def guardar_archivo(user_id, archivo_data, descripcion):
    if not archivo_data or not archivo_data.filename:
        return None
    try:
        filename = secure_filename(archivo_data.filename)
        unique_filename = f"{int(time.time())}_{user_id}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        archivo_data.save(file_path)
        
        categoria = 'pdf' if filename.lower().endswith('.pdf') else 'imagen'
        
        cursor = db.connection.cursor()
        sql = "INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (user_id, categoria, descripcion, unique_filename))
        db.connection.commit()
        return cursor.lastrowid
    except Exception as ex:
        logging.error(f"Error al guardar archivo para user {user_id}: {ex}")
        flash('Ocurrió un error al intentar guardar un archivo.', 'danger')
        return None

# --- RUTA PRINCIPAL Y RUTAS AUXILIARES ---
@docente_bp.route('/home')
@login_required
def home():
    return render_template('home.html')

@docente_bp.route('/get_universidades', methods=['POST'])
@login_required
def get_universidades():
    data = request.get_json()
    pais = data.get('pais', 'Perú')
    country_universities = { 'Perú': ['Universidad Nacional Del Altiplano', 'Otra'], 'Otro': ['Otra'] }
    universidades = country_universities.get(pais, ['Otra'])
    return jsonify(universidades)

@docente_bp.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# =================================================================
# === IMPLEMENTACIÓN CRUD COMPLETA PARA CADA SECCIÓN DEL CV ===
# =================================================================

# --- 1. Información Personal ---
@docente_bp.route('/informacion_personal', methods=['GET', 'POST'])
@login_required
def informacion_personal():
    # Esta ruta es especial, solo actualiza.
    datos_actuales = ModelCV.obtener_datos_personales(db, current_user.id)
    form = InformacionPersonalForm(data=datos_actuales)
    if form.validate_on_submit():
        try:
            id_foto = guardar_archivo(current_user.id, form.foto_docente.data, "Foto de Docente")
            id_constancia = guardar_archivo(current_user.id, form.constancia_habilitacion.data, "Constancia de Habilitación")
            ModelCV.actualizar_datos_personales(db, current_user.id, form, id_foto, id_constancia, datos_actuales)
            flash('Información personal actualizada.', 'success')
            return redirect(url_for('docente.home'))
        except Exception as ex:
            flash(str(ex), 'danger')
    return render_template('informacion_personal.html', form=form, datos_actuales=datos_actuales)

# --- 2. Grados y Títulos ---
@docente_bp.route('/gradostitulos', methods=['GET', 'POST'])
@login_required
def gradostitulos():
    form = GradostitulosForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.titulo.data)
        id_img_sunedu = guardar_archivo(current_user.id, form.archivo_sunedu.data, f"SUNEDU - {form.titulo.data}")
        ModelCV.crear_grado(db, current_user.id, form, id_img, id_img_sunedu)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.gradostitulos'))
    items = ModelCV.obtener_grados_por_usuario(db, current_user.id)
    return render_template('gradostitulos.html', gradostitulos=items, form=form)

@docente_bp.route('/gradostitulos/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_gradostitulos(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'gradostitulos', 'id_grado', id_item, current_user.id)
    form = GradostitulosForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.titulo.data)
        id_img_sunedu = guardar_archivo(current_user.id, form.archivo_sunedu.data, f"SUNEDU - {form.titulo.data}")
        ModelCV.actualizar_grado(db, id_item, form, id_img, id_img_sunedu)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.gradostitulos'))
    return render_template('editar_gradostitulos.html', form=form, item=item)

@docente_bp.route('/gradostitulos/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_gradostitulos(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'gradostitulos', 'id_grado', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.gradostitulos'))

# --- 3. Experiencia Docente ---
@docente_bp.route('/experienciadocente', methods=['GET', 'POST'])
@login_required
def experienciadocente():
    form = ExperienciaDocenteForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.descripcion.data)
        ModelCV.crear_experiencia(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.experienciadocente'))
    items = ModelCV.obtener_experiencias_por_usuario(db, current_user.id)
    return render_template('experienciadocente.html', experiencias=items, form=form)

@docente_bp.route('/experienciadocente/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_experienciadocente(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'experienciadocente', 'id_experiencia', id_item, current_user.id)
    form = ExperienciaDocenteForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.descripcion.data)
        ModelCV.actualizar_experiencia(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.experienciadocente'))
    return render_template('editar_experienciadocente.html', form=form, experiencia=item)

@docente_bp.route('/experienciadocente/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_experienciadocente(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'experienciadocente', 'id_experiencia', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.experienciadocente'))

# --- Repetir el patrón para TODAS las demás secciones ---

# 4. Investigaciones
@docente_bp.route('/investigaciones', methods=['GET', 'POST'])
@login_required
def investigaciones():
    form = InvestigacionesForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.titulo.data)
        ModelCV.crear_investigacion(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.investigaciones'))
    items = ModelCV.obtener_investigaciones_por_usuario(db, current_user.id)
    return render_template('investigaciones.html', investigaciones=items, form=form)

@docente_bp.route('/investigaciones/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_investigacion(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'investigaciones', 'id_investigacion', id_item, current_user.id)
    form = InvestigacionesForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.titulo.data)
        ModelCV.actualizar_investigacion(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.investigaciones'))
    return render_template('editar_investigacion.html', form=form, investigacion=item)

@docente_bp.route('/investigaciones/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_investigacion(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'investigaciones', 'id_investigacion', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.investigaciones'))

# 5. Producción Intelectual
@docente_bp.route('/produccion_intelectual', methods=['GET', 'POST'])
@login_required
def produccion_intelectual():
    form = ProduccionIntelectualForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.titulo.data)
        ModelCV.crear_produccion(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.produccion_intelectual'))
    items = ModelCV.obtener_producciones_por_usuario(db, current_user.id)
    return render_template('produccion_intelectual.html', producciones=items, form=form)

@docente_bp.route('/produccion_intelectual/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_produccion_intelectual(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'produccionintelectual', 'id_produccion', id_item, current_user.id)
    form = ProduccionIntelectualForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.titulo.data)
        ModelCV.actualizar_produccion(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.produccion_intelectual'))
    return render_template('editar_produccion_intelectual.html', form=form, produccion=item)

@docente_bp.route('/produccion_intelectual/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_produccion_intelectual(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'produccionintelectual', 'id_produccion', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.produccion_intelectual'))

# 6. Actualizaciones y Capacitaciones
@docente_bp.route('/actualizacionescapacitaciones', methods=['GET', 'POST'])
@login_required
def actualizacionescapacitaciones():
    form = ActualizacionesCapacitacionesForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.descripcion.data)
        ModelCV.crear_capacitacion(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.actualizacionescapacitaciones'))
    items = ModelCV.obtener_capacitaciones_por_usuario(db, current_user.id)
    return render_template('actualizacionescapacitaciones.html', actualizaciones=items, form=form)

@docente_bp.route('/actualizacionescapacitaciones/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_actualizacioncapacitacion(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'actualizacionescapacitaciones', 'id_capacitacion', id_item, current_user.id)
    form = ActualizacionesCapacitacionesForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.descripcion.data)
        ModelCV.actualizar_capacitacion(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.actualizacionescapacitaciones'))
    return render_template('editar_actualizacioncapacitacion.html', form=form, actualizacion=item)

@docente_bp.route('/actualizacionescapacitaciones/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_actualizacioncapacitacion(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'actualizacionescapacitaciones', 'id_capacitacion', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.actualizacionescapacitaciones'))

# ... (El código anterior termina con las rutas para Actualizaciones y Capacitaciones) ...

# =================================================================
# === CONTINUACIÓN DEL CRUD PARA LAS 10 SECCIONES RESTANTES ===
# =================================================================

# --- 7. Cargos Directivos ---
@docente_bp.route('/cargosdirectivos', methods=['GET', 'POST'])
@login_required
def cargosdirectivos():
    form = CargosDirectivosForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.cargo.data)
        ModelCV.crear_cargo_directivo(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.cargosdirectivos'))
    items = ModelCV.obtener_cargos_directivos_por_usuario(db, current_user.id)
    return render_template('cargosdirectivos.html', cargos=items, form=form)

@docente_bp.route('/cargosdirectivos/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_cargosdirectivos(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'cargosdirectivos', 'id_cargo', id_item, current_user.id)
    if not item: return redirect(url_for('docente.cargosdirectivos'))
    form = CargosDirectivosForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.cargo.data)
        ModelCV.actualizar_cargo_directivo(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.cargosdirectivos'))
    return render_template('editar_cargosdirectivos.html', form=form, cargo=item)

@docente_bp.route('/cargosdirectivos/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_cargosdirectivos(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'cargosdirectivos', 'id_cargo', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.cargosdirectivos'))


# --- 8. Participación en Tesis ---
@docente_bp.route('/participaciontesis', methods=['GET', 'POST'])
@login_required
def participaciontesis():
    form = ParticipacionTesisForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.descripcion.data)
        ModelCV.crear_participacion_tesis(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.participaciontesis'))
    items = ModelCV.obtener_participaciones_tesis_por_usuario(db, current_user.id)
    return render_template('participaciontesis.html', participaciontesis=items, form=form)

@docente_bp.route('/participaciontesis/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_participaciontesis(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'participaciontesis', 'id_participaciontesis', id_item, current_user.id)
    if not item: return redirect(url_for('docente.participaciontesis'))
    form = ParticipacionTesisForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.descripcion.data)
        ModelCV.actualizar_participacion_tesis(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.participaciontesis'))
    return render_template('editar_participaciontesis.html', form=form, participacion=item)

@docente_bp.route('/participaciontesis/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_participaciontesis(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'participaciontesis', 'id_participaciontesis', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.participaciontesis'))


# --- 9. Reconocimientos y Distinciones ---
@docente_bp.route('/reconocimientos', methods=['GET', 'POST'])
@login_required
def reconocimientos():
    form = ReconocimientosForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.descripcion.data)
        ModelCV.crear_reconocimiento(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.reconocimientos'))
    items = ModelCV.obtener_reconocimientos_por_usuario(db, current_user.id)
    return render_template('reconocimientos.html', reconocimientos=items, form=form)

@docente_bp.route('/reconocimientos/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_reconocimiento(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'reconocimientos', 'id_reconocimiento', id_item, current_user.id)
    if not item: return redirect(url_for('docente.reconocimientos'))
    form = ReconocimientosForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.descripcion.data)
        ModelCV.actualizar_reconocimiento(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.reconocimientos'))
    return render_template('editar_reconocimiento.html', form=form, reconocimiento=item)

@docente_bp.route('/reconocimientos/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_reconocimiento(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'reconocimientos', 'id_reconocimiento', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.reconocimientos'))


# --- 10. Idiomas ---
@docente_bp.route('/idiomas', methods=['GET', 'POST'])
@login_required
def idiomas():
    form = IdiomasForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, f"Certificado de {form.idioma.data}")
        ModelCV.crear_idioma(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.idiomas'))
    items = ModelCV.obtener_idiomas_por_usuario(db, current_user.id)
    return render_template('idiomas.html', idiomas=items, form=form)

@docente_bp.route('/idiomas/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_idioma(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'idiomas', 'id_idioma', id_item, current_user.id)
    if not item: return redirect(url_for('docente.idiomas'))
    form = IdiomasForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, f"Certificado de {form.idioma.data}")
        ModelCV.actualizar_idioma(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.idiomas'))
    return render_template('editar_idioma.html', form=form, idioma=item)

@docente_bp.route('/idiomas/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_idioma(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'idiomas', 'id_idioma', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.idiomas'))


# --- 11. Software Especializado ---
@docente_bp.route('/softwareespecializado', methods=['GET', 'POST'])
@login_required
def softwareespecializado():
    form = SoftwareEspecializadoForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.nombre_curso.data)
        ModelCV.crear_software(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.softwareespecializado'))
    items = ModelCV.obtener_softwares_por_usuario(db, current_user.id)
    return render_template('softwareespecializado.html', softwareespecializados=items, form=form)

@docente_bp.route('/softwareespecializado/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_softwareespecializado(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'softwareespecializado', 'id_software', id_item, current_user.id)
    if not item: return redirect(url_for('docente.softwareespecializado'))
    form = SoftwareEspecializadoForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, form.nombre_curso.data)
        ModelCV.actualizar_software(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.softwareespecializado'))
    return render_template('editar_softwareespecializado.html', form=form, software=item)

@docente_bp.route('/softwareespecializado/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_softwareespecializado(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'softwareespecializado', 'id_software', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.softwareespecializado'))


# --- 12. Tutorías ---
@docente_bp.route('/tutorias', methods=['GET', 'POST'])
@login_required
def tutorias():
    form = TutoriaForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, f"Tutoría {form.semestre.data}")
        ModelCV.crear_tutoria(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.tutorias'))
    items = ModelCV.obtener_tutorias_por_usuario(db, current_user.id)
    return render_template('tutorias.html', tutorias=items, form=form)

@docente_bp.route('/tutorias/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_tutoria(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'tutorias', 'id_tutoria', id_item, current_user.id)
    if not item: return redirect(url_for('docente.tutorias'))
    form = TutoriaForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, f"Tutoría {form.semestre.data}")
        ModelCV.actualizar_tutoria(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.tutorias'))
    return render_template('editar_tutoria.html', form=form, tutoria=item)

@docente_bp.route('/tutorias/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_tutoria(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'tutorias', 'id_tutoria', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.tutorias'))


# --- 13. Carga Académica Lectiva ---
@docente_bp.route('/carga_academica', methods=['GET', 'POST'])
@login_required
def carga_academica():
    form = CargaAcademicaLectivaForm()
    if form.validate_on_submit():
        id_memo = guardar_archivo(current_user.id, form.archivo_memorandum.data, form.numero_memorandum.data)
        ModelCV.crear_carga_academica(db, current_user.id, form, id_memo)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.carga_academica'))
    items = ModelCV.obtener_cargas_academicas_por_usuario(db, current_user.id)
    return render_template('carga_academica.html', cargas=items, form=form)

@docente_bp.route('/carga_academica/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_carga_academica(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'carga_academica_lectiva', 'id_carga', id_item, current_user.id)
    if not item: return redirect(url_for('docente.carga_academica'))
    form = CargaAcademicaLectivaForm(data=item)
    if form.validate_on_submit():
        id_memo = guardar_archivo(current_user.id, form.archivo_memorandum.data, form.numero_memorandum.data)
        ModelCV.actualizar_carga_academica(db, id_item, form, id_memo)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.carga_academica'))
    return render_template('editar_carga_academica.html', form=form, carga=item)

@docente_bp.route('/carga_academica/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_carga_academica(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'carga_academica_lectiva', 'id_carga', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.carga_academica'))


# --- 14. Participación en Gestión Universitaria ---
@docente_bp.route('/participaciongestionuniversitaria', methods=['GET', 'POST'])
@login_required
def participaciongestionuniversitaria():
    form = ParticipacionGestionUniversitariaForm()
    if form.validate_on_submit():
        id_plan = guardar_archivo(current_user.id, form.adjuntar_plan.data, f"Plan - {form.cargo.data}")
        id_informe = guardar_archivo(current_user.id, form.adjuntar_informe.data, f"Informe - {form.cargo.data}")
        id_curso = guardar_archivo(current_user.id, form.adjuntar_curso.data, f"Curso - {form.cargo.data}")
        ModelCV.crear_gestion_universitaria(db, current_user.id, form, id_plan, id_informe, id_curso)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.participaciongestionuniversitaria'))
    items = ModelCV.obtener_gestiones_universitarias_por_usuario(db, current_user.id)
    return render_template('participaciongestionuniversitaria.html', participaciones=items, form=form)

@docente_bp.route('/participaciongestionuniversitaria/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_participaciongestionuniversitaria(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'participaciongestionuniversitaria', 'id', id_item, current_user.id)
    if not item: return redirect(url_for('docente.participaciongestionuniversitaria'))
    form = ParticipacionGestionUniversitariaForm(data=item)
    if form.validate_on_submit():
        id_plan = guardar_archivo(current_user.id, form.adjuntar_plan.data, f"Plan - {form.cargo.data}")
        id_informe = guardar_archivo(current_user.id, form.adjuntar_informe.data, f"Informe - {form.cargo.data}")
        id_curso = guardar_archivo(current_user.id, form.adjuntar_curso.data, f"Curso - {form.cargo.data}")
        ModelCV.actualizar_gestion_universitaria(db, id_item, form, id_plan, id_informe, id_curso)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.participaciongestionuniversitaria'))
    return render_template('editar_participaciongestionuniversitaria.html', form=form, participacion=item)

@docente_bp.route('/participaciongestionuniversitaria/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_participaciongestionuniversitaria(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'participaciongestionuniversitaria', 'id', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.participaciongestionuniversitaria'))


# --- 15. Acreditación y Licenciamiento ---
@docente_bp.route('/acreditacionlicenciamiento', methods=['GET', 'POST'])
@login_required
def acreditacionlicenciamiento():
    form = AcreditacionLicenciamientoForm()
    if form.validate_on_submit():
        id_res = guardar_archivo(current_user.id, form.archivo_resolucion.data, f"Resolución {form.numero_resolucion.data}")
        id_evi = guardar_archivo(current_user.id, form.evidencias.data, f"Evidencias - {form.numero_resolucion.data}")
        ModelCV.crear_acreditacion(db, current_user.id, form, id_res, id_evi)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.acreditacionlicenciamiento'))
    items = ModelCV.obtener_acreditaciones_por_usuario(db, current_user.id)
    return render_template('acreditacion_licenciamiento.html', acreditaciones=items, form=form)

@docente_bp.route('/acreditacionlicenciamiento/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_acreditacionlicenciamiento(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'acreditacionlicenciamiento', 'id_acreditacion', id_item, current_user.id)
    if not item: return redirect(url_for('docente.acreditacionlicenciamiento'))
    form = AcreditacionLicenciamientoForm(data=item)
    if form.validate_on_submit():
        id_res = guardar_archivo(current_user.id, form.archivo_resolucion.data, f"Resolución {form.numero_resolucion.data}")
        id_evi = guardar_archivo(current_user.id, form.evidencias.data, f"Evidencias - {form.numero_resolucion.data}")
        ModelCV.actualizar_acreditacion(db, id_item, form, id_res, id_evi)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.acreditacionlicenciamiento'))
    return render_template('editar_acreditacion_licenciamiento.html', form=form, acreditacion=item)

@docente_bp.route('/acreditacionlicenciamiento/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_acreditacionlicenciamiento(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'acreditacionlicenciamiento', 'id_acreditacion', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.acreditacionlicenciamiento'))


# --- 16. Actividades de Proyección Social ---
@docente_bp.route('/actividadesproyeccionsocial', methods=['GET', 'POST'])
@login_required
def actividadesproyeccionsocial():
    form = ActividadesProyeccionSocialForm()
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, f"Proyección Social - {form.Emitido_por.data}")
        ModelCV.crear_proyeccion_social(db, current_user.id, form, id_img)
        flash('Registro agregado.', 'success')
        return redirect(url_for('docente.actividadesproyeccionsocial'))
    items = ModelCV.obtener_proyecciones_sociales_por_usuario(db, current_user.id)
    return render_template('actividadesproyeccionsocial.html', actividades=items, form=form)

@docente_bp.route('/actividadesproyeccionsocial/editar/<int:id_item>', methods=['GET', 'POST'])
@login_required
def editar_actividadesproyeccionsocial(id_item):
    item = ModelCV.obtener_registro_por_id(db, 'actividadesproyeccionsocial', 'id_actividad', id_item, current_user.id)
    if not item: return redirect(url_for('docente.actividadesproyeccionsocial'))
    form = ActividadesProyeccionSocialForm(data=item)
    if form.validate_on_submit():
        id_img = guardar_archivo(current_user.id, form.archivo.data, f"Proyección Social - {form.Emitido_por.data}")
        ModelCV.actualizar_proyeccion_social(db, id_item, form, id_img)
        flash('Registro actualizado.', 'success')
        return redirect(url_for('docente.actividadesproyeccionsocial'))
    return render_template('editar_actividadesproyeccionsocial.html', form=form, actividad=item)

@docente_bp.route('/actividadesproyeccionsocial/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_actividadesproyeccionsocial(id_item):
    ModelCV.eliminar_registro(db, app.config['UPLOAD_FOLDER'], 'actividadesproyeccionsocial', 'id_actividad', id_item, current_user.id)
    flash('Registro eliminado.', 'success')
    return redirect(url_for('docente.actividadesproyeccionsocial'))