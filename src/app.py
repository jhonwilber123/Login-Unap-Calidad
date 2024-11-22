# src/app.py
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import time
import bcrypt
import MySQLdb.cursors
import re

from config import config

# Importar el formulario
from forms import TutoriaForm, SoftwareEspecializadoForm, ReconocimientosForm, ProduccionIntelectualForm, ParticipacionTesisForm 
from forms import InvestigacionesForm, IdiomasForm, GradostitulosForm, ActividadesProyeccionSocialForm 
from forms import ActualizacionesCapacitacionesForm, CargosDirectivosForm, ExperienciaDocenteForm, InformacionPersonalForm

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

# Configuración de Flask
app = Flask(__name__)

# Configuración para subir archivos
UPLOAD_FOLDER = 'uploads/'  # Carpeta donde se guardarán las imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}  # Tipos de archivo permitidos
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
# Limitar el tamaño máximo de la carga a 100 MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 Megabytes


csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user is not None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña inválida.")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado.")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Ruta para el home
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/change-password', methods=['GET', 'POST']) 
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Verificar que la nueva contraseña y la confirmación coinciden
        if new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden.')
            return redirect(url_for('change_password'))

        # Verificar que la contraseña actual es correcta
        user = ModelUser.get_by_id(db, current_user.id)
        if not User.check_password(user.password, current_password):
            flash('La contraseña actual es incorrecta.')
            return redirect(url_for('change_password'))

        # Verificar que la nueva contraseña sea segura
        reasons = []
        if len(new_password) < 8:
            reasons.append("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', new_password):
            reasons.append("La contraseña debe tener al menos una letra mayúscula.")
        if not re.search(r'[a-z]', new_password):
            reasons.append("La contraseña debe tener al menos una letra minúscula.")
        if not re.search(r'\d', new_password):
            reasons.append("La contraseña debe tener al menos un número.")
        
        if reasons:
            for reason in reasons:
                flash(reason)
            return redirect(url_for('change_password'))

        # Actualizar la contraseña en la base de datos
        hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        success = ModelUser.update_password(db, current_user.id, hashed_new_password)

        if success:
            flash('Tu contraseña ha sido actualizada exitosamente.')
            return redirect(url_for('home'))
        else:
            flash('Hubo un error al actualizar tu contraseña. Intenta nuevamente.')
            return redirect(url_for('change_password'))
    else:
        return render_template('auth/change_password.html')

@app.route('/validate-password', methods=['POST'])
@login_required
def validate_password():
    password = request.form['password']
    reasons = []
    if len(password) < 8:
        reasons.append("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r'[A-Z]', password):
        reasons.append("La contraseña debe tener al menos una letra mayúscula.")
    if not re.search(r'[a-z]', password):
        reasons.append("La contraseña debe tener al menos una letra minúscula.")
    if not re.search(r'\d', password):
        reasons.append("La contraseña debe tener al menos un número.")
    
    return jsonify({'valid': len(reasons) == 0, 'reasons': reasons})

# --- NUEVAS RUTAS ---

# Ruta para editar datos personales
@app.route('/informacion_personal', methods=['GET', 'POST'])
@login_required
def informacion_personal():
    form = InformacionPersonalForm()
    
    if form.validate_on_submit():
        # Manejar la carga de foto de docente
        id_foto_docente = None
        foto_docente = form.foto_docente.data
        if foto_docente:
            filename = secure_filename(foto_docente.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            foto_docente.save(file_path)
            
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("""
                INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                VALUES (%s, 'imagen', 'Foto de Docente', %s)
            """, (current_user.id, unique_filename))
            db.connection.commit()
            id_foto_docente = cur.lastrowid
            cur.close()

        # Manejar la carga de constancia de habilitación
        id_constancia_habilitacion = None
        constancia_habilitacion = form.constancia_habilitacion.data
        if constancia_habilitacion:
            filename = secure_filename(constancia_habilitacion.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            constancia_habilitacion.save(file_path)
            
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("""
                INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                VALUES (%s, 'documento', 'Constancia de Habilitación', %s)
            """, (current_user.id, unique_filename))
            db.connection.commit()
            id_constancia_habilitacion = cur.lastrowid
            cur.close()

        # Capturar datos del formulario
        data = {
            'apellido_paterno': form.apellido_paterno.data,
            'apellido_materno': form.apellido_materno.data,
            'nombres': form.nombres.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'lugar_nacimiento_departamento': form.lugar_nacimiento_departamento.data,
            'lugar_nacimiento_provincia': form.lugar_nacimiento_provincia.data,
            'lugar_nacimiento_distrito': form.lugar_nacimiento_distrito.data,
            'dni': form.dni.data,
            'numero_colegiatura': form.numero_colegiatura.data or '',
            'codigo': form.codigo.data,
            'condicion': form.condicion.data,
            'categoria': form.categoria.data,
            'dedicacion': form.dedicacion.data,
            'telefono_fijo': form.telefono_fijo.data,
            'movil': form.movil.data,
            'correo_personal': form.correo_personal.data,
            'correo_institucional': form.correo_institucional.data,
            'domicilio_actual': form.domicilio_actual.data,
            'referencia': form.referencia.data or '',
            'id_foto_docente': id_foto_docente,
            'id_constancia_habilitacion': id_constancia_habilitacion
        }

        # Verificar si ya existen datos personales para el usuario
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT id_datos FROM datospersonales WHERE id_usuario = %s", [current_user.id])
        existing_data = cur.fetchone()

        if existing_data:
            # Actualizar datos existentes
            cur.execute("""
                UPDATE datospersonales SET 
                    apellido_paterno=%(apellido_paterno)s, 
                    apellido_materno=%(apellido_materno)s, 
                    nombres=%(nombres)s, 
                    fecha_nacimiento=%(fecha_nacimiento)s,
                    lugar_nacimiento_departamento=%(lugar_nacimiento_departamento)s, 
                    lugar_nacimiento_provincia=%(lugar_nacimiento_provincia)s, 
                    lugar_nacimiento_distrito=%(lugar_nacimiento_distrito)s, 
                    dni=%(dni)s,
                    numero_colegiatura=%(numero_colegiatura)s, 
                    codigo=%(codigo)s, 
                    condicion=%(condicion)s, 
                    categoria=%(categoria)s,
                    dedicacion=%(dedicacion)s, 
                    telefono_fijo=%(telefono_fijo)s, 
                    movil=%(movil)s, 
                    correo_personal=%(correo_personal)s, 
                    correo_institucional=%(correo_institucional)s,
                    domicilio_actual=%(domicilio_actual)s, 
                    referencia=%(referencia)s,
                    id_foto_docente=%(id_foto_docente)s,
                    id_constancia_habilitacion=%(id_constancia_habilitacion)s
                WHERE id_usuario=%(id_usuario)s
            """, {**data, 'id_usuario': current_user.id})
        else:
            # Insertar nuevos datos
            cur.execute("""
                INSERT INTO datospersonales (
                    id_usuario, 
                    apellido_paterno, 
                    apellido_materno, 
                    nombres, 
                    fecha_nacimiento,
                    lugar_nacimiento_departamento, 
                    lugar_nacimiento_provincia, 
                    lugar_nacimiento_distrito, 
                    dni,
                    numero_colegiatura, 
                    codigo, 
                    condicion, 
                    categoria,
                    dedicacion, 
                    telefono_fijo, 
                    movil, 
                    correo_personal, 
                    correo_institucional,
                    domicilio_actual, 
                    referencia,
                    id_foto_docente,
                    id_constancia_habilitacion
                ) VALUES (
                    %(id_usuario)s, 
                    %(apellido_paterno)s, 
                    %(apellido_materno)s, 
                    %(nombres)s, 
                    %(fecha_nacimiento)s,
                    %(lugar_nacimiento_departamento)s, 
                    %(lugar_nacimiento_provincia)s, 
                    %(lugar_nacimiento_distrito)s, 
                    %(dni)s,
                    %(numero_colegiatura)s, 
                    %(codigo)s, 
                    %(condicion)s, 
                    %(categoria)s,
                    %(dedicacion)s, 
                    %(telefono_fijo)s, 
                    %(movil)s, 
                    %(correo_personal)s, 
                    %(correo_institucional)s,
                    %(domicilio_actual)s, 
                    %(referencia)s,
                    %(id_foto_docente)s,
                    %(id_constancia_habilitacion)s
                )
            """, {**data, 'id_usuario': current_user.id})
        
        db.connection.commit()
        cur.close()
        flash('Información personal actualizada correctamente', 'success')
        return redirect(url_for('home'))
    
    # Obtener datos personales actuales para prellenar el formulario
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT dp.*, 
        foto.ruta_imagen AS foto_ruta, 
        constancia.ruta_imagen AS constancia_ruta 
        FROM datospersonales dp
        LEFT JOIN imagenesadjuntas foto ON dp.id_foto_docente = foto.id_imagen
        LEFT JOIN imagenesadjuntas constancia ON dp.id_constancia_habilitacion = constancia.id_imagen
        WHERE dp.id_usuario = %s
    """, [current_user.id])
    existing_data = cur.fetchone()
    cur.close()

    if existing_data and request.method == 'GET':
        # Prellenar datos del formulario
        form.apellido_paterno.data = existing_data['apellido_paterno']
        form.apellido_materno.data = existing_data['apellido_materno']
        form.nombres.data = existing_data['nombres']
        form.fecha_nacimiento.data = existing_data['fecha_nacimiento']
        form.lugar_nacimiento_departamento.data = existing_data['lugar_nacimiento_departamento']
        form.lugar_nacimiento_provincia.data = existing_data['lugar_nacimiento_provincia']
        form.lugar_nacimiento_distrito.data = existing_data['lugar_nacimiento_distrito']
        form.dni.data = existing_data['dni']
        form.numero_colegiatura.data = existing_data['numero_colegiatura']
        form.codigo.data = existing_data['codigo']
        form.condicion.data = existing_data['condicion']
        form.categoria.data = existing_data['categoria']
        form.dedicacion.data = existing_data['dedicacion']
        form.telefono_fijo.data = existing_data['telefono_fijo']
        form.movil.data = existing_data['movil']
        form.correo_personal.data = existing_data['correo_personal']
        form.correo_institucional.data = existing_data['correo_institucional']
        form.domicilio_actual.data = existing_data['domicilio_actual']
        form.referencia.data = existing_data['referencia']

    return render_template('informacion_personal.html', form=form, 
                           foto_url=existing_data.get('foto_ruta') if existing_data else None,
                           constancia_url=existing_data.get('constancia_ruta') if existing_data else None)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Ruta del archivo: {file_path}")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta para listar y agregar grados y títulos
# Ruta para editar un grado/título
# Ruta para agregar un nuevo grado/título con imagen
# Ruta para servir las imágenes

# --- RUTA PARA AGREGAR Y LISTAR TÍTULOS ---
# --- RUTA PARA AGREGAR Y LISTAR TÍTULOS ---
@app.route('/gradostitulos', methods=['GET', 'POST'])
@login_required
def gradostitulos():
    form = GradostitulosForm()
    if form.validate_on_submit():
        titulo = form.titulo.data
        tipo = form.tipo.data
        universidad = form.universidad.data
        otro_universidad = form.otro_universidad.data
        pais = form.pais.data
        otro_pais = form.otro_pais.data
        fecha_expedicion = form.fecha_expedicion.data

        # Manejo de "Otra Universidad"
        if universidad == 'Otra':
            universidad = otro_universidad

        # Manejo de "Otro País"
        if pais == 'Otro':
            pais = otro_pais

        # Manejo de archivos (imagen o PDF)
        archivo = form.archivo.data
        id_imagen = None
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, titulo, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar el título académico
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO gradostitulos (id_usuario, titulo, tipo, universidad, pais, fecha_expedicion, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, titulo, tipo, universidad, pais, fecha_expedicion, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Título académico agregado correctamente', 'success')
        return redirect(url_for('gradostitulos'))

    # Obtener los títulos académicos del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT gt.id_grado, gt.titulo, gt.tipo, gt.universidad, gt.pais, gt.fecha_expedicion,
               ia.ruta_imagen, ia.categoria
        FROM gradostitulos gt
        LEFT JOIN imagenesadjuntas ia ON gt.id_imagen = ia.id_imagen
        WHERE gt.id_usuario = %s
    """, [current_user.id])
    gradostitulos = cur.fetchall()
    cur.close()

    return render_template('gradostitulos.html', gradostitulos=gradostitulos, form=form)

# --- RUTA PARA EDITAR UN TÍTULO ---
@app.route('/editar_gradostitulos/<int:id_grado>', methods=['GET', 'POST'])
@login_required
def editar_gradostitulos(id_grado):
    form = GradostitulosForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales del título
    cur.execute("""
        SELECT gt.id_grado, gt.titulo, gt.tipo, gt.universidad, gt.pais, gt.fecha_expedicion,
               ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM gradostitulos gt
        LEFT JOIN imagenesadjuntas ia ON gt.id_imagen = ia.id_imagen
        WHERE gt.id_grado = %s AND gt.id_usuario = %s
    """, (id_grado, current_user.id))
    grado = cur.fetchone()
    cur.close()

    if not grado:
        flash('Título académico no encontrado', 'danger')
        return redirect(url_for('gradostitulos'))

    if form.validate_on_submit():
        titulo = form.titulo.data
        tipo = form.tipo.data
        universidad = form.universidad.data
        otro_universidad = form.otro_universidad.data
        pais = form.pais.data
        otro_pais = form.otro_pais.data
        fecha_expedicion = form.fecha_expedicion.data
        archivo = form.archivo.data
        id_imagen_actual = grado['id_imagen']

        # Manejo de "Otra Universidad"
        if universidad == 'Otra':
            universidad = otro_universidad

        # Manejo de "Otro País"
        if pais == 'Otro':
            pais = otro_pais

        # Manejo del archivo adjunto
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                if id_imagen_actual:
                    # Actualizar el archivo existente
                    cur.execute("""
                        UPDATE imagenesadjuntas
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, titulo, id_imagen_actual, current_user.id))
                else:
                    # Insertar un nuevo archivo
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, titulo, unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Actualizar el título con el nuevo id_imagen
                    cur.execute("""
                        UPDATE gradostitulos
                        SET id_imagen = %s
                        WHERE id_grado = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_grado, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Actualizar los datos del título académico
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE gradostitulos
            SET titulo = %s, tipo = %s, universidad = %s, pais = %s, fecha_expedicion = %s
            WHERE id_grado = %s AND id_usuario = %s
        """, (titulo, tipo, universidad, pais, fecha_expedicion, id_grado, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Título académico actualizado correctamente', 'success')
        return redirect(url_for('gradostitulos'))

    # Prellenar el formulario con los datos actuales
    if request.method == 'GET':
        form.titulo.data = grado['titulo']
        form.tipo.data = grado['tipo']
        # Manejar "Otra Universidad"
        predefined_universidades = ['Universidad Nacional Del Altiplano', 'Universidad Peruana Cayetano Heredia']
        if grado['universidad'] not in predefined_universidades:
            form.universidad.data = 'Otra'
            form.otro_universidad.data = grado['universidad']
        else:
            form.universidad.data = grado['universidad']
            form.otro_universidad.data = ''

        # Manejar "Otro País"
        predefined_paises = ['Perú', 'Chile']
        if grado['pais'] not in predefined_paises:
            form.pais.data = 'Otro'
            form.otro_pais.data = grado['pais']
        else:
            form.pais.data = grado['pais']
            form.otro_pais.data = ''

        form.fecha_expedicion.data = grado['fecha_expedicion']

    return render_template('editar_gradostitulos.html', grado=grado, form=form)

# --- RUTA PARA ELIMINAR UN TÍTULO ---
@app.route('/eliminar_gradostitulos/<int:id_grado>', methods=['POST'])
@login_required
def eliminar_gradostitulos(id_grado):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM gradostitulos
        WHERE id_grado = %s AND id_usuario = %s
    """, (id_grado, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar el archivo físico del servidor
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()
        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
            # Eliminar la imagen de la tabla imagenesadjuntas
            cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
            db.connection.commit()

    # Eliminar el título académico
    cur.execute("DELETE FROM gradostitulos WHERE id_grado = %s AND id_usuario = %s", (id_grado, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Título académico eliminado correctamente', 'success')
    return redirect(url_for('gradostitulos'))

# Ruta para manejar actividades de proyección social
# --- RUTA PARA AGREGAR Y LISTAR ACTIVIDADES DE PROYECCIÓN SOCIAL ---
@app.route('/actividadesproyeccionsocial', methods=['GET', 'POST'])
@login_required
def actividadesproyeccionsocial():
    form = ActividadesProyeccionSocialForm()
    if form.validate_on_submit():
        tipo = form.tipo.data
        evento = form.evento.data
        descripcion = form.descripcion.data
        fecha = form.fecha.data

        # Manejo de archivos (imagen o PDF)
        archivo = form.archivo.data
        id_imagen = None
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar la actividad de proyección social sin 'nivel'
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO actividadesproyeccionsocial (id_usuario, tipo, evento, descripcion, fecha, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, evento, descripcion, fecha, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Actividad de proyección social agregada correctamente', 'success')
        return redirect(url_for('actividadesproyeccionsocial'))

    # Obtener las actividades de proyección social del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT aps.id_actividad, aps.tipo, aps.evento, aps.descripcion, aps.fecha,
               ia.ruta_imagen, ia.categoria
        FROM actividadesproyeccionsocial aps
        LEFT JOIN imagenesadjuntas ia ON aps.id_imagen = ia.id_imagen
        WHERE aps.id_usuario = %s
    """, [current_user.id])
    actividades = cur.fetchall()
    cur.close()

    return render_template('actividadesproyeccionsocial.html', actividades=actividades, form=form)

# --- RUTA PARA EDITAR UNA ACTIVIDAD DE PROYECCIÓN SOCIAL ---
@app.route('/editar_actividadesproyeccionsocial/<int:id_actividad>', methods=['GET', 'POST'])
@login_required
def editar_actividadesproyeccionsocial(id_actividad):
    form = ActividadesProyeccionSocialForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales de la actividad
    cur.execute("""
        SELECT aps.id_actividad, aps.tipo, aps.evento, aps.descripcion, aps.fecha,
               ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM actividadesproyeccionsocial aps
        LEFT JOIN imagenesadjuntas ia ON aps.id_imagen = ia.id_imagen
        WHERE aps.id_actividad = %s AND aps.id_usuario = %s
    """, (id_actividad, current_user.id))
    actividad = cur.fetchone()
    cur.close()

    if not actividad:
        flash('Actividad de proyección social no encontrada', 'danger')
        return redirect(url_for('actividadesproyeccionsocial'))

    if form.validate_on_submit():
        tipo = form.tipo.data
        evento = form.evento.data
        descripcion = form.descripcion.data
        fecha = form.fecha.data
        archivo = form.archivo.data
        id_imagen_actual = actividad['id_imagen']

        # Manejo del archivo adjunto
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                if id_imagen_actual:
                    # Actualizar el archivo existente
                    cur.execute("""
                        UPDATE imagenesadjuntas
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, descripcion, id_imagen_actual, current_user.id))
                else:
                    # Insertar un nuevo archivo
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, descripcion, unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Actualizar la actividad con el nuevo id_imagen
                    cur.execute("""
                        UPDATE actividadesproyeccionsocial
                        SET id_imagen = %s
                        WHERE id_actividad = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_actividad, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Actualizar los datos de la actividad de proyección social sin 'nivel'
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE actividadesproyeccionsocial
            SET tipo = %s, evento = %s, descripcion = %s, fecha = %s
            WHERE id_actividad = %s AND id_usuario = %s
        """, (tipo, evento, descripcion, fecha, id_actividad, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Actividad de proyección social actualizada correctamente', 'success')
        return redirect(url_for('actividadesproyeccionsocial'))

    # Prellenar el formulario con los datos actuales
    if request.method == 'GET':
        form.tipo.data = actividad['tipo']
        form.evento.data = actividad['evento']
        form.descripcion.data = actividad['descripcion']
        form.fecha.data = actividad['fecha']

    return render_template('editar_actividadesproyeccionsocial.html', actividad=actividad, form=form)

# --- RUTA PARA ELIMINAR UNA ACTIVIDAD DE PROYECCIÓN SOCIAL ---
@app.route('/eliminar_actividadesproyeccionsocial/<int:id_actividad>', methods=['POST'])
@login_required
def eliminar_actividadesproyeccionsocial(id_actividad):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM actividadesproyeccionsocial
        WHERE id_actividad = %s AND id_usuario = %s
    """, (id_actividad, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar el archivo físico del servidor
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()
        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
            # Eliminar la imagen de la tabla imagenesadjuntas
            cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
            db.connection.commit()

    # Eliminar la actividad de proyección social
    cur.execute("DELETE FROM actividadesproyeccionsocial WHERE id_actividad = %s AND id_usuario = %s", (id_actividad, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Actividad de proyección social eliminada correctamente', 'success')
    return redirect(url_for('actividadesproyeccionsocial'))

# Nueva Ruta para manejar Actualizaciones y Capacitaciones
# --- RUTA PARA AGREGAR Y LISTAR ACTUALIZACIONES DE CAPACITACIONES ---
# --- RUTA PARA AGREGAR Y LISTAR ACTUALIZACIONES DE CAPACITACIONES ---
@app.route('/actualizacionescapacitaciones', methods=['GET', 'POST'])
@login_required
def actualizacionescapacitaciones():
    form = ActualizacionesCapacitacionesForm()
    if form.validate_on_submit():
        tipo = form.tipo.data
        descripcion = form.descripcion.data
        horas = form.horas.data if form.horas.data else None
        creditos = form.creditos.data if form.creditos.data else None
        semestres_concluidos = form.semestres_concluidos.data if form.semestres_concluidos.data else None

        # Manejo de archivos (imagen o PDF)
        archivo = form.archivo.data
        id_imagen = None
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar la actualización de capacitación
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO actualizacionescapacitaciones (id_usuario, tipo, descripcion, horas, creditos, semestres_concluidos, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, descripcion, horas, creditos, semestres_concluidos, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Actualización de capacitación agregada correctamente', 'success')
        return redirect(url_for('actualizacionescapacitaciones'))

    # Obtener las actualizaciones de capacitaciones del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT ac.id_capacitacion, ac.tipo, ac.descripcion, ac.horas, ac.creditos, ac.semestres_concluidos,
               ia.ruta_imagen, ia.categoria
        FROM actualizacionescapacitaciones ac
        LEFT JOIN imagenesadjuntas ia ON ac.id_imagen = ia.id_imagen
        WHERE ac.id_usuario = %s
    """, [current_user.id])
    actualizaciones = cur.fetchall()
    cur.close()

    return render_template('actualizacionescapacitaciones.html', actualizaciones=actualizaciones, form=form)

# --- RUTA PARA EDITAR UNA ACTUALIZACIÓN DE CAPACITACIÓN ---
@app.route('/editar_actualizacioncapacitacion/<int:id_capacitacion>', methods=['GET', 'POST'])
@login_required
def editar_actualizacioncapacitacion(id_capacitacion):
    form = ActualizacionesCapacitacionesForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales de la actualización
    cur.execute("""
        SELECT ac.id_capacitacion, ac.tipo, ac.descripcion, ac.horas, ac.creditos, ac.semestres_concluidos,
               ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM actualizacionescapacitaciones ac
        LEFT JOIN imagenesadjuntas ia ON ac.id_imagen = ia.id_imagen
        WHERE ac.id_capacitacion = %s AND ac.id_usuario = %s
    """, (id_capacitacion, current_user.id))
    actualizacion = cur.fetchone()
    cur.close()

    if not actualizacion:
        flash('Actualización de capacitación no encontrada', 'danger')
        return redirect(url_for('actualizacionescapacitaciones'))

    if form.validate_on_submit():
        tipo = form.tipo.data
        descripcion = form.descripcion.data
        horas = form.horas.data if form.horas.data else None
        creditos = form.creditos.data if form.creditos.data else None
        semestres_concluidos = form.semestres_concluidos.data if form.semestres_concluidos.data else None
        archivo = form.archivo.data
        id_imagen_actual = actualizacion['id_imagen']

        # Manejo del archivo adjunto
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                if id_imagen_actual:
                    # Actualizar el archivo existente
                    cur.execute("""
                        UPDATE imagenesadjuntas
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, descripcion, id_imagen_actual, current_user.id))
                else:
                    # Insertar un nuevo archivo
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, descripcion, unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Actualizar la actualización de capacitación con el nuevo id_imagen
                    cur.execute("""
                        UPDATE actualizacionescapacitaciones
                        SET id_imagen = %s
                        WHERE id_capacitacion = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_capacitacion, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Actualizar los datos de la actualización de capacitación
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE actualizacionescapacitaciones
            SET tipo = %s, descripcion = %s, horas = %s, creditos = %s, semestres_concluidos = %s
            WHERE id_capacitacion = %s AND id_usuario = %s
        """, (tipo, descripcion, horas, creditos, semestres_concluidos, id_capacitacion, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Actualización de capacitación actualizada correctamente', 'success')
        return redirect(url_for('actualizacionescapacitaciones'))

    # Prellenar el formulario con los datos actuales
    if request.method == 'GET':
        form.tipo.data = actualizacion['tipo']
        form.descripcion.data = actualizacion['descripcion']
        form.horas.data = actualizacion['horas']
        form.creditos.data = actualizacion['creditos']
        form.semestres_concluidos.data = actualizacion['semestres_concluidos']

    return render_template('editar_actualizacioncapacitacion.html', actualizacion=actualizacion, form=form)

# --- RUTA PARA ELIMINAR UNA ACTUALIZACIÓN DE CAPACITACIÓN ---
@app.route('/eliminar_actualizacioncapacitacion/<int:id_capacitacion>', methods=['POST'])
@login_required
def eliminar_actualizacioncapacitacion(id_capacitacion):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM actualizacionescapacitaciones
        WHERE id_capacitacion = %s AND id_usuario = %s
    """, (id_capacitacion, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar el archivo físico del servidor
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()
        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
            # Eliminar la imagen de la tabla imagenesadjuntas
            cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
            db.connection.commit()

    # Eliminar la actualización de capacitación
    cur.execute("DELETE FROM actualizacionescapacitaciones WHERE id_capacitacion = %s AND id_usuario = %s", (id_capacitacion, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Actualización de capacitación eliminada correctamente', 'success')
    return redirect(url_for('actualizacionescapacitaciones'))

# Ruta para listar y agregar cargos directivos
# --- RUTA PARA AGREGAR Y LISTAR CARGOS DIRECTIVOS ---
@app.route('/cargosdirectivos', methods=['GET', 'POST'])
@login_required
def cargosdirectivos():
    form = CargosDirectivosForm()
    if form.validate_on_submit():
        cargo = form.cargo.data
        anios = form.anios.data
        descripcion = form.descripcion.data

        # Manejo de archivos (imagen o PDF)
        archivo = form.archivo.data
        id_imagen = None
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar el cargo directivo
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO cargosdirectivos (id_usuario, cargo, anios, id_imagen)
            VALUES (%s, %s, %s, %s)
        """, (current_user.id, cargo, anios, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Cargo directivo agregado correctamente', 'success')
        return redirect(url_for('cargosdirectivos'))

    # Obtener los cargos directivos del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT cd.id_cargo, cd.cargo, cd.anios, cd.descripcion,
               ia.ruta_imagen, ia.categoria
        FROM cargosdirectivos cd
        LEFT JOIN imagenesadjuntas ia ON cd.id_imagen = ia.id_imagen
        WHERE cd.id_usuario = %s
    """, [current_user.id])
    cargos = cur.fetchall()
    cur.close()

    return render_template('cargosdirectivos.html', cargos=cargos, form=form)

# --- RUTA PARA EDITAR UN CARGO DIRECTIVO ---
@app.route('/editar_cargo/<int:id_cargo>', methods=['GET', 'POST'])
@login_required
def editar_cargo(id_cargo):
    form = CargosDirectivosForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales del cargo
    cur.execute("""
        SELECT cd.id_cargo, cd.cargo, cd.anios, cd.descripcion,
               ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM cargosdirectivos cd
        LEFT JOIN imagenesadjuntas ia ON cd.id_imagen = ia.id_imagen
        WHERE cd.id_cargo = %s AND cd.id_usuario = %s
    """, (id_cargo, current_user.id))
    cargo = cur.fetchone()
    cur.close()

    if not cargo:
        flash('Cargo directivo no encontrado', 'danger')
        return redirect(url_for('cargosdirectivos'))

    if form.validate_on_submit():
        cargo_nuevo = form.cargo.data
        anios = form.anios.data
        descripcion = form.descripcion.data
        archivo = form.archivo.data
        id_imagen_actual = cargo['id_imagen']

        # Manejo del archivo adjunto
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                if id_imagen_actual:
                    # Actualizar el archivo existente
                    cur.execute("""
                        UPDATE imagenesadjuntas
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, descripcion, id_imagen_actual, current_user.id))
                else:
                    # Insertar un nuevo archivo
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, descripcion, unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Actualizar el cargo con el nuevo id_imagen
                    cur.execute("""
                        UPDATE cargosdirectivos
                        SET id_imagen = %s
                        WHERE id_cargo = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_cargo, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Actualizar los datos del cargo directivo
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE cargosdirectivos
            SET cargo = %s, anios = %s, descripcion = %s
            WHERE id_cargo = %s AND id_usuario = %s
        """, (cargo_nuevo, anios, descripcion, id_cargo, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Cargo directivo actualizado correctamente', 'success')
        return redirect(url_for('cargosdirectivos'))

    # Prellenar el formulario con los datos actuales
    if request.method == 'GET':
        form.cargo.data = cargo['cargo']
        form.anios.data = cargo['anios']
        form.descripcion.data = cargo['descripcion']

    return render_template('editar_cargosdirectivos.html', cargo=cargo, form=form)

# --- RUTA PARA ELIMINAR UN CARGO DIRECTIVO ---
@app.route('/eliminar_cargo/<int:id_cargo>', methods=['POST'])
@login_required
def eliminar_cargo(id_cargo):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM cargosdirectivos
        WHERE id_cargo = %s AND id_usuario = %s
    """, (id_cargo, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar el archivo físico del servidor
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()
        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
            # Eliminar la imagen de la tabla imagenesadjuntas
            cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
            db.connection.commit()

    # Eliminar el cargo directivo
    cur.execute("DELETE FROM cargosdirectivos WHERE id_cargo = %s AND id_usuario = %s", (id_cargo, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Cargo directivo eliminado correctamente', 'success')
    return redirect(url_for('cargosdirectivos'))


# Ruta para listar y agregar experiencia docente
# --- RUTA PARA AGREGAR Y LISTAR EXPERIENCIAS DOCENTES ---
@app.route('/experienciadocente', methods=['GET', 'POST'])
@login_required
def experienciadocente():
    form = ExperienciaDocenteForm()
    if form.validate_on_submit():
        tipo = form.tipo.data
        descripcion = form.descripcion.data
        anios = form.anios.data
        cursos = form.cursos.data

        # Manejo de archivos (imagen o PDF)
        archivo = form.archivo.data
        id_imagen = None
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar la experiencia docente
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO experienciadocente (id_usuario, tipo, descripcion, anios, cursos, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, descripcion, anios, cursos, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Experiencia docente agregada correctamente', 'success')
        return redirect(url_for('experienciadocente'))

    # Obtener las experiencias docentes del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT ed.id_experiencia, ed.tipo, ed.descripcion, ed.anios, ed.cursos,
               ia.ruta_imagen, ia.categoria
        FROM experienciadocente ed
        LEFT JOIN imagenesadjuntas ia ON ed.id_imagen = ia.id_imagen
        WHERE ed.id_usuario = %s
    """, [current_user.id])
    experiencias = cur.fetchall()
    cur.close()

    return render_template('experienciadocente.html', experiencias=experiencias, form=form)

# --- RUTA PARA EDITAR UNA EXPERIENCIA DOCENTE ---
@app.route('/editar_experienciadocente/<int:id_experiencia>', methods=['GET', 'POST'])
@login_required
def editar_experienciadocente(id_experiencia):
    form = ExperienciaDocenteForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales de la experiencia
    cur.execute("""
        SELECT ed.id_experiencia, ed.tipo, ed.descripcion, ed.anios, ed.cursos,
               ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM experienciadocente ed
        LEFT JOIN imagenesadjuntas ia ON ed.id_imagen = ia.id_imagen
        WHERE ed.id_experiencia = %s AND ed.id_usuario = %s
    """, (id_experiencia, current_user.id))
    experiencia = cur.fetchone()
    cur.close()

    if not experiencia:
        flash('Experiencia docente no encontrada', 'danger')
        return redirect(url_for('experienciadocente'))

    if form.validate_on_submit():
        tipo = form.tipo.data
        descripcion = form.descripcion.data
        anios = form.anios.data
        cursos = form.cursos.data
        archivo = form.archivo.data
        id_imagen_actual = experiencia['id_imagen']

        # Manejo del archivo adjunto
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                if id_imagen_actual:
                    # Actualizar el archivo existente
                    cur.execute("""
                        UPDATE imagenesadjuntas
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, descripcion, id_imagen_actual, current_user.id))
                else:
                    # Insertar un nuevo archivo
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, descripcion, unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Actualizar la experiencia docente con el nuevo id_imagen
                    cur.execute("""
                        UPDATE experienciadocente
                        SET id_imagen = %s
                        WHERE id_experiencia = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_experiencia, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Actualizar los datos de la experiencia docente
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE experienciadocente
            SET tipo = %s, descripcion = %s, anios = %s, cursos = %s
            WHERE id_experiencia = %s AND id_usuario = %s
        """, (tipo, descripcion, anios, cursos, id_experiencia, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Experiencia docente actualizada correctamente', 'success')
        return redirect(url_for('experienciadocente'))

    # Prellenar el formulario con los datos actuales
    if request.method == 'GET':
        form.tipo.data = experiencia['tipo']
        form.descripcion.data = experiencia['descripcion']
        form.anios.data = experiencia['anios']
        form.cursos.data = experiencia['cursos']

    return render_template('editar_experienciadocente.html', experiencia=experiencia, form=form)

# --- RUTA PARA ELIMINAR UNA EXPERIENCIA DOCENTE ---
@app.route('/eliminar_experienciadocente/<int:id_experiencia>', methods=['POST'])
@login_required
def eliminar_experienciadocente(id_experiencia):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM experienciadocente
        WHERE id_experiencia = %s AND id_usuario = %s
    """, (id_experiencia, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar el archivo físico del servidor
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()
        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
            # Eliminar la imagen de la tabla imagenesadjuntas
            cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
            db.connection.commit()

    # Eliminar la experiencia docente
    cur.execute("DELETE FROM experienciadocente WHERE id_experiencia = %s AND id_usuario = %s", (id_experiencia, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Experiencia docente eliminada correctamente', 'success')
    return redirect(url_for('experienciadocente'))


# --- NUEVA RUTA PARA IDIOMAS ---

# --- RUTA PARA AGREGAR Y LISTAR IDIOMAS ---
@app.route('/idiomas', methods=['GET', 'POST'])
@login_required
def idiomas():
    form = IdiomasForm()
    if form.validate_on_submit():
        # Manejar la selección del idioma
        if form.idioma.data == 'Otro':
            idioma = form.otro_idioma.data.strip()
            if not idioma:
                flash('Debe especificar el otro idioma.', 'danger')
                return redirect(request.url)
        else:
            idioma = form.idioma.data

        nivel = form.nivel.data
        certificado = form.certificado.data
        archivo = form.archivo.data
        id_imagen = None

        if certificado and archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, f'Certificado de {idioma}', unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar el idioma
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO idiomas (id_usuario, idioma, nivel, certificado, id_imagen)
            VALUES (%s, %s, %s, %s, %s)
        """, (current_user.id, idioma, nivel, certificado, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Idioma agregado correctamente', 'success')
        return redirect(url_for('idiomas'))

    # Obtener los idiomas del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT i.id_idioma, i.idioma, i.nivel, i.certificado, ia.ruta_imagen, ia.categoria
        FROM idiomas i
        LEFT JOIN imagenesadjuntas ia ON i.id_imagen = ia.id_imagen
        WHERE i.id_usuario = %s
    """, [current_user.id])
    idiomas_list = cur.fetchall()
    cur.close()

    return render_template('idiomas.html', idiomas=idiomas_list, form=form)

# --- RUTA PARA EDITAR UN IDIOMA ---
@app.route('/editar_idioma/<int:id_idioma>', methods=['GET', 'POST'])
@login_required
def editar_idioma(id_idioma):
    form = IdiomasForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales del idioma
    cur.execute("""
        SELECT i.id_idioma, i.idioma, i.nivel, i.certificado, ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM idiomas i
        LEFT JOIN imagenesadjuntas ia ON i.id_imagen = ia.id_imagen
        WHERE i.id_idioma = %s AND i.id_usuario = %s
    """, (id_idioma, current_user.id))
    idioma = cur.fetchone()
    cur.close()

    if not idioma:
        flash('Idioma no encontrado', 'danger')
        return redirect(url_for('idiomas'))

    if form.validate_on_submit():
        # Manejar la selección del idioma
        if form.idioma.data == 'Otro':
            nuevo_idioma = form.otro_idioma.data.strip()
            if not nuevo_idioma:
                flash('Debe especificar el otro idioma.', 'danger')
                return redirect(request.url)
        else:
            nuevo_idioma = form.idioma.data

        nivel = form.nivel.data
        certificado = form.certificado.data
        archivo = form.archivo.data
        id_imagen_actual = idioma['id_imagen']

        # Manejo del archivo adjunto
        if certificado and archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                if id_imagen_actual:
                    # Actualizar el archivo existente
                    cur.execute("""
                        UPDATE imagenesadjuntas
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, f'Certificado de {nuevo_idioma}', id_imagen_actual, current_user.id))
                else:
                    # Insertar un nuevo archivo
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, f'Certificado de {nuevo_idioma}', unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Actualizar el idioma con el nuevo id_imagen
                    cur.execute("""
                        UPDATE idiomas
                        SET id_imagen = %s
                        WHERE id_idioma = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_idioma, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)
        elif not certificado and idioma['id_imagen']:
            # Si el usuario desmarca el certificado, eliminar el archivo asociado
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("""
                SELECT ruta_imagen FROM imagenesadjuntas
                WHERE id_imagen = %s AND id_usuario = %s
            """, (idioma['id_imagen'], current_user.id))
            imagen = cur.fetchone()
            if imagen:
                ruta_imagen = imagen['ruta_imagen']
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
                if os.path.exists(file_path):
                    os.remove(file_path)
                # Eliminar la imagen de la tabla imagenesadjuntas
                cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (idioma['id_imagen'], current_user.id))
                db.connection.commit()
            cur.close()
            id_imagen_actual = None

        # Actualizar los datos del idioma
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE idiomas
            SET idioma = %s, nivel = %s, certificado = %s
            WHERE id_idioma = %s AND id_usuario = %s
        """, (nuevo_idioma, nivel, certificado, id_idioma, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Idioma actualizado correctamente', 'success')
        return redirect(url_for('idiomas'))

    # Prellenar el formulario con los datos actuales
    if request.method == 'GET':
        # Determinar si el idioma actual es uno de los predefinidos
        predefinidos = ['Inglés', 'Francés', 'Alemán', 'Italiano', 'Portugués']
        if idioma['idioma'] in predefinidos:
            form.idioma.data = idioma['idioma']
            form.otro_idioma.data = ''
        else:
            form.idioma.data = 'Otro'
            form.otro_idioma.data = idioma['idioma']
        form.nivel.data = idioma['nivel']
        form.certificado.data = idioma['certificado']

    return render_template('editar_idioma.html', idioma=idioma, form=form)

# --- RUTA PARA ELIMINAR UN IDIOMA ---
@app.route('/eliminar_idioma/<int:id_idioma>', methods=['POST'])
@login_required
def eliminar_idioma(id_idioma):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM idiomas
        WHERE id_idioma = %s AND id_usuario = %s
    """, (id_idioma, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar el archivo físico del servidor
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()
        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
            # Eliminar la imagen de la tabla imagenesadjuntas
            cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
            db.connection.commit()

    # Eliminar el idioma
    cur.execute("DELETE FROM idiomas WHERE id_idioma = %s AND id_usuario = %s", (id_idioma, current_user.id))
    db.connection.commit()
    cur.close()

    flash('Idioma eliminado correctamente', 'success')
    return redirect(url_for('idiomas'))

# --- NUEVA RUTA PARA INVESTIGACIONES ---

# --- RUTA PARA AGREGAR Y LISTAR INVESTIGACIONES ---
@app.route('/investigaciones', methods=['GET', 'POST'])
@login_required
def investigaciones():
    form = InvestigacionesForm()
    if form.validate_on_submit():
        tipo = form.tipo.data
        titulo = form.titulo.data
        descripcion = form.descripcion.data
        fecha_inicio = form.fecha_inicio.data
        fecha_fin = form.fecha_fin.data
        revista = form.revista.data
        indice = form.indice.data
        fecha_publicacion = form.fecha_publicacion.data
        autor = form.autor.data
        coautor = form.coautor.data

        # Manejo de archivos (imagen o PDF)
        archivo = form.archivo.data
        id_imagen = None
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar la investigación
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO investigaciones (id_usuario, tipo, titulo, descripcion, fecha_inicio, fecha_fin, revista, indice, fecha_publicacion, autor, coautor, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            current_user.id, tipo, titulo, descripcion,
            fecha_inicio, fecha_fin, revista, indice,
            fecha_publicacion, autor, coautor, id_imagen
        ))
        db.connection.commit()
        cur.close()

        flash('Investigación agregada correctamente', 'success')
        return redirect(url_for('investigaciones'))

    # Obtener las investigaciones del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT i.id_investigacion, i.tipo, i.titulo, i.descripcion, i.fecha_inicio, i.fecha_fin,
               i.revista, i.indice, i.fecha_publicacion, i.autor, i.coautor,
               ia.ruta_imagen, ia.categoria
        FROM investigaciones i
        LEFT JOIN imagenesadjuntas ia ON i.id_imagen = ia.id_imagen
        WHERE i.id_usuario = %s
    """, [current_user.id])
    investigaciones = cur.fetchall()
    cur.close()

    return render_template('investigaciones.html', investigaciones=investigaciones, form=form)

# --- RUTA PARA EDITAR UNA INVESTIGACIÓN ---
@app.route('/editar_investigacion/<int:id_investigacion>', methods=['GET', 'POST'])
@login_required
def editar_investigacion(id_investigacion):
    form = InvestigacionesForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales de la investigación
    cur.execute("""
        SELECT i.id_investigacion, i.tipo, i.titulo, i.descripcion, i.fecha_inicio, i.fecha_fin,
               i.revista, i.indice, i.fecha_publicacion, i.autor, i.coautor,
               ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM investigaciones i
        LEFT JOIN imagenesadjuntas ia ON i.id_imagen = ia.id_imagen
        WHERE i.id_investigacion = %s AND i.id_usuario = %s
    """, (id_investigacion, current_user.id))
    investigacion = cur.fetchone()
    cur.close()

    if not investigacion:
        flash('Investigación no encontrada', 'danger')
        return redirect(url_for('investigaciones'))

    if form.validate_on_submit():
        tipo = form.tipo.data
        titulo = form.titulo.data
        descripcion = form.descripcion.data
        fecha_inicio = form.fecha_inicio.data
        fecha_fin = form.fecha_fin.data
        revista = form.revista.data
        indice = form.indice.data
        fecha_publicacion = form.fecha_publicacion.data
        autor = form.autor.data
        coautor = form.coautor.data
        archivo = form.archivo.data
        id_imagen_actual = investigacion['id_imagen']

        # Manejo del archivo adjunto
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                if id_imagen_actual:
                    # Actualizar el archivo existente
                    cur.execute("""
                        UPDATE imagenesadjuntas
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, descripcion, id_imagen_actual, current_user.id))
                else:
                    # Insertar un nuevo archivo
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, descripcion, unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Actualizar la investigación con el nuevo id_imagen
                    cur.execute("""
                        UPDATE investigaciones
                        SET id_imagen = %s
                        WHERE id_investigacion = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_investigacion, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Actualizar los datos de la investigación
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE investigaciones
            SET tipo = %s, titulo = %s, descripcion = %s, fecha_inicio = %s,
                fecha_fin = %s, revista = %s, indice = %s,
                fecha_publicacion = %s, autor = %s, coautor = %s
            WHERE id_investigacion = %s AND id_usuario = %s
        """, (
            tipo, titulo, descripcion, fecha_inicio,
            fecha_fin, revista, indice,
            fecha_publicacion, autor, coautor,
            id_investigacion, current_user.id
        ))
        db.connection.commit()
        cur.close()

        flash('Investigación actualizada correctamente', 'success')
        return redirect(url_for('investigaciones'))

    # Prellenar el formulario con los datos actuales
    if request.method == 'GET':
        form.tipo.data = investigacion['tipo']
        form.titulo.data = investigacion['titulo']
        form.descripcion.data = investigacion['descripcion']
        form.fecha_inicio.data = investigacion['fecha_inicio']
        form.fecha_fin.data = investigacion['fecha_fin']
        form.revista.data = investigacion['revista']
        form.indice.data = investigacion['indice']
        form.fecha_publicacion.data = investigacion['fecha_publicacion']
        form.autor.data = investigacion['autor']
        form.coautor.data = investigacion['coautor']

    return render_template('editar_investigacion.html', investigacion=investigacion, form=form)

# --- RUTA PARA ELIMINAR UNA INVESTIGACIÓN ---
@app.route('/eliminar_investigacion/<int:id_investigacion>', methods=['POST'])
@login_required
def eliminar_investigacion(id_investigacion):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM investigaciones
        WHERE id_investigacion = %s AND id_usuario = %s
    """, (id_investigacion, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar el archivo físico del servidor
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()
        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
            # Eliminar la imagen de la tabla imagenesadjuntas
            cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
            db.connection.commit()

    # Eliminar la investigación
    cur.execute("DELETE FROM investigaciones WHERE id_investigacion = %s AND id_usuario = %s", (id_investigacion, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Investigación eliminada correctamente', 'success')
    return redirect(url_for('investigaciones'))

# --- RUTAS PARA PARTICIPACIONTESIS ---

@app.route('/participaciontesis', methods=['GET', 'POST'])
@login_required
def participaciontesis():
    form = ParticipacionTesisForm()
    if form.validate_on_submit():
        tipo = form.tipo.data
        nivel = form.nivel.data
        descripcion = form.descripcion.data
        universidad = form.universidad.data
        fecha = form.fecha.data

        # Manejo de archivos (imagen o PDF)
        archivo = form.archivo.data
        id_imagen = None
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar la participación en tesis
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO participaciontesis (id_usuario, tipo, nivel, descripcion, universidad, fecha, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, nivel, descripcion, universidad, fecha, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Participación en tesis agregada correctamente', 'success')
        return redirect(url_for('participaciontesis'))

    # Obtener las participaciones en tesis del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT pt.id_participaciontesis, pt.tipo, pt.nivel, pt.descripcion, pt.universidad, pt.fecha,
               ia.ruta_imagen, ia.categoria
        FROM participaciontesis pt
        LEFT JOIN imagenesadjuntas ia ON pt.id_imagen = ia.id_imagen
        WHERE pt.id_usuario = %s
    """, [current_user.id])
    participaciontesis = cur.fetchall()
    cur.close()

    return render_template('participaciontesis.html', participaciontesis=participaciontesis, form=form)

# --- RUTA PARA EDITAR UNA PARTICIPACIÓN EN TESIS ---
@app.route('/editar_participaciontesis/<int:id_participaciontesis>', methods=['GET', 'POST'])
@login_required
def editar_participaciontesis(id_participaciontesis):
    form = ParticipacionTesisForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales de la participación en tesis
    cur.execute("""
        SELECT pt.id_participaciontesis, pt.tipo, pt.nivel, pt.descripcion, pt.universidad, pt.fecha,
               ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM participaciontesis pt
        LEFT JOIN imagenesadjuntas ia ON pt.id_imagen = ia.id_imagen
        WHERE pt.id_participaciontesis = %s AND pt.id_usuario = %s
    """, (id_participaciontesis, current_user.id))
    participacion = cur.fetchone()
    cur.close()

    if not participacion:
        flash('Participación en tesis no encontrada', 'danger')
        return redirect(url_for('participaciontesis'))

    if form.validate_on_submit():
        tipo = form.tipo.data
        nivel = form.nivel.data
        descripcion = form.descripcion.data
        universidad = form.universidad.data
        fecha = form.fecha.data
        archivo = form.archivo.data
        id_imagen_actual = participacion['id_imagen']

        # Manejo del archivo adjunto
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                if id_imagen_actual:
                    # Actualizar el archivo existente
                    cur.execute("""
                        UPDATE imagenesadjuntas
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, descripcion, id_imagen_actual, current_user.id))
                else:
                    # Insertar un nuevo archivo
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, descripcion, unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Actualizar la participación con el nuevo id_imagen
                    cur.execute("""
                        UPDATE participaciontesis
                        SET id_imagen = %s
                        WHERE id_participaciontesis = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_participaciontesis, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Actualizar los datos de la participación en tesis
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE participaciontesis
            SET tipo = %s, nivel = %s, descripcion = %s, universidad = %s, fecha = %s
            WHERE id_participaciontesis = %s AND id_usuario = %s
        """, (tipo, nivel, descripcion, universidad, fecha, id_participaciontesis, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Participación en tesis actualizada correctamente', 'success')
        return redirect(url_for('participaciontesis'))

    # Prellenar el formulario con los datos actuales
    if request.method == 'GET':
        form.tipo.data = participacion['tipo']
        form.nivel.data = participacion['nivel']
        form.descripcion.data = participacion['descripcion']
        form.universidad.data = participacion['universidad']
        form.fecha.data = participacion['fecha']

    return render_template('editar_participaciontesis.html', participacion=participacion, form=form)

# --- RUTA PARA ELIMINAR UNA PARTICIPACIÓN EN TESIS ---
@app.route('/eliminar_participaciontesis/<int:id_participaciontesis>', methods=['POST'])
@login_required
def eliminar_participaciontesis(id_participaciontesis):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM participaciontesis
        WHERE id_participaciontesis = %s AND id_usuario = %s
    """, (id_participaciontesis, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar el archivo físico del servidor
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()
        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
            # Eliminar la imagen de la tabla imagenesadjuntas
            cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
            db.connection.commit()

    # Eliminar la participación en tesis
    cur.execute("DELETE FROM participaciontesis WHERE id_participaciontesis = %s AND id_usuario = %s", (id_participaciontesis, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Participación en tesis eliminada correctamente', 'success')
    return redirect(url_for('participaciontesis'))



# --- NUEVA RUTA PARA PRODUCCIÓN INTELECTUAL ---

# Ruta para agregar y listar producciones intelectuales
@app.route('/produccion_intelectual', methods=['GET', 'POST'])
@login_required
def produccion_intelectual():
    form = ProduccionIntelectualForm()
    if form.validate_on_submit():
        tipo = form.tipo.data
        titulo = form.titulo.data
        isbn = form.isbn.data
        deposito_legal = form.deposito_legal.data
        fecha_publicacion = form.fecha_publicacion.data
        autor = form.autor.data
        coautor = form.coautor.data
        editorial_prestigiosa = form.editorial_prestigiosa.data  # Nuevo campo

        # Manejo de archivos (imagen o PDF)
        archivo = form.archivo.data
        id_imagen = None
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, titulo, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar la producción intelectual
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO produccionintelectual
            (id_usuario, tipo, titulo, isbn, deposito_legal, fecha_publicacion, autor, coautor, editorial_prestigiosa, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, titulo, isbn, deposito_legal, fecha_publicacion, autor, coautor, editorial_prestigiosa, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Producción intelectual agregada correctamente', 'success')
        return redirect(url_for('produccion_intelectual'))

    # Obtener las producciones intelectuales del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT p.id_produccion, p.tipo, p.titulo, p.isbn, p.deposito_legal, p.fecha_publicacion, p.autor, p.coautor,
               p.editorial_prestigiosa, ia.ruta_imagen, ia.categoria
        FROM produccionintelectual p
        LEFT JOIN imagenesadjuntas ia ON p.id_imagen = ia.id_imagen
        WHERE p.id_usuario = %s
    """, [current_user.id])
    producciones = cur.fetchall()
    cur.close()

    return render_template('produccion_intelectual.html', producciones=producciones, form=form)

# Ruta para editar una producción intelectual
@app.route('/editar_produccion_intelectual/<int:id_produccion>', methods=['GET', 'POST'])
@login_required
def editar_produccion_intelectual(id_produccion):
    form = ProduccionIntelectualForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales de la producción intelectual
    cur.execute("""
        SELECT p.id_produccion, p.tipo, p.titulo, p.isbn, p.deposito_legal, p.fecha_publicacion, p.autor, p.coautor,
               p.editorial_prestigiosa, ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM produccionintelectual p
        LEFT JOIN imagenesadjuntas ia ON p.id_imagen = ia.id_imagen
        WHERE p.id_produccion = %s AND p.id_usuario = %s
    """, (id_produccion, current_user.id))
    produccion = cur.fetchone()
    cur.close()

    if not produccion:
        flash('Producción intelectual no encontrada', 'danger')
        return redirect(url_for('produccion_intelectual'))

    if form.validate_on_submit():
        tipo = form.tipo.data
        titulo = form.titulo.data
        isbn = form.isbn.data
        deposito_legal = form.deposito_legal.data
        fecha_publicacion = form.fecha_publicacion.data
        autor = form.autor.data
        coautor = form.coautor.data
        editorial_prestigiosa = form.editorial_prestigiosa.data  # Nuevo campo
        archivo = form.archivo.data
        id_imagen_actual = produccion['id_imagen']

        # Manejo del archivo adjunto
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                if id_imagen_actual:
                    # Actualizar el archivo existente
                    cur.execute("""
                        UPDATE imagenesadjuntas
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, titulo, id_imagen_actual, current_user.id))
                else:
                    # Insertar un nuevo archivo
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, titulo, unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Actualizar la producción intelectual con el nuevo id_imagen
                    cur.execute("""
                        UPDATE produccionintelectual
                        SET id_imagen = %s
                        WHERE id_produccion = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_produccion, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Actualizar los datos de la producción intelectual
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE produccionintelectual
            SET tipo = %s, titulo = %s, isbn = %s, deposito_legal = %s, fecha_publicacion = %s, autor = %s, coautor = %s, editorial_prestigiosa = %s
            WHERE id_produccion = %s AND id_usuario = %s
        """, (tipo, titulo, isbn, deposito_legal, fecha_publicacion, autor, coautor, editorial_prestigiosa, id_produccion, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Producción intelectual actualizada correctamente', 'success')
        return redirect(url_for('produccion_intelectual'))

    # Prellenar el formulario con los datos actuales
    if request.method == 'GET':
        form.tipo.data = produccion['tipo']
        form.titulo.data = produccion['titulo']
        form.isbn.data = produccion['isbn']
        form.deposito_legal.data = bool(produccion['deposito_legal'])
        form.fecha_publicacion.data = produccion['fecha_publicacion']
        form.autor.data = bool(produccion['autor'])
        form.coautor.data = bool(produccion['coautor'])
        form.editorial_prestigiosa.data = produccion['editorial_prestigiosa']  # Nuevo campo

    return render_template('editar_produccion_intelectual.html', produccion=produccion, form=form)

# Ruta para eliminar una producción intelectual
@app.route('/eliminar_produccion_intelectual/<int:id_produccion>', methods=['POST'])
@login_required
def eliminar_produccion_intelectual(id_produccion):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM produccionintelectual
        WHERE id_produccion = %s AND id_usuario = %s
    """, (id_produccion, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Obtener la ruta de la imagen
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()

        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            # Eliminar el archivo físico si existe
            if os.path.exists(file_path):
                os.remove(file_path)
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))

    # Eliminar la producción intelectual
    cur.execute("DELETE FROM produccionintelectual WHERE id_produccion = %s AND id_usuario = %s", (id_produccion, current_user.id))
    db.connection.commit()
    cur.close()

    flash('Producción intelectual eliminada correctamente', 'success')
    return redirect(url_for('produccion_intelectual'))


# --- NUEVA RUTA PARA RECONOCIMIENTOS ---

# --- RUTA PARA AGREGAR Y LISTAR RECONOCIMIENTOS ---
@app.route('/reconocimientos', methods=['GET', 'POST'])
@login_required
def reconocimientos():
    form = ReconocimientosForm()
    if form.validate_on_submit():
        tipo = form.tipo.data
        tipo_institucion = form.tipo_institucion.data
        descripcion = form.descripcion.data
        institucion = form.institucion.data
        fecha = form.fecha.data

        # Manejo de archivos (imagen o PDF)
        archivo = form.archivo.data
        id_imagen = None
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar el reconocimiento
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO reconocimientos (id_usuario, tipo, descripcion, institucion, tipo_institucion, fecha, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, descripcion, institucion, tipo_institucion, fecha, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Reconocimiento agregado correctamente', 'success')
        return redirect(url_for('reconocimientos'))

    # Obtener los reconocimientos del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT r.id_reconocimiento, r.tipo, r.descripcion, r.institucion, r.tipo_institucion, r.fecha,
               ia.ruta_imagen, ia.categoria
        FROM reconocimientos r
        LEFT JOIN imagenesadjuntas ia ON r.id_imagen = ia.id_imagen
        WHERE r.id_usuario = %s
    """, [current_user.id])
    reconocimientos = cur.fetchall()
    cur.close()

    return render_template('reconocimientos.html', reconocimientos=reconocimientos, form=form)

# --- RUTA PARA EDITAR UN RECONOCIMIENTO ---
@app.route('/editar_reconocimiento/<int:id_reconocimiento>', methods=['GET', 'POST'])
@login_required
def editar_reconocimiento(id_reconocimiento):
    form = ReconocimientosForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales del reconocimiento
    cur.execute("""
        SELECT r.id_reconocimiento, r.tipo, r.descripcion, r.institucion, r.tipo_institucion, r.fecha,
               ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM reconocimientos r
        LEFT JOIN imagenesadjuntas ia ON r.id_imagen = ia.id_imagen
        WHERE r.id_reconocimiento = %s AND r.id_usuario = %s
    """, (id_reconocimiento, current_user.id))
    reconocimiento = cur.fetchone()
    cur.close()

    if not reconocimiento:
        flash('Reconocimiento no encontrado', 'danger')
        return redirect(url_for('reconocimientos'))

    if form.validate_on_submit():
        tipo = form.tipo.data
        tipo_institucion = form.tipo_institucion.data
        descripcion = form.descripcion.data
        institucion = form.institucion.data
        fecha = form.fecha.data
        archivo = form.archivo.data
        id_imagen_actual = reconocimiento['id_imagen']

        # Manejo del archivo adjunto
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                if id_imagen_actual:
                    # Actualizar el archivo existente
                    cur.execute("""
                        UPDATE imagenesadjuntas
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, descripcion, id_imagen_actual, current_user.id))
                else:
                    # Insertar un nuevo archivo
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen)
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, descripcion, unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Actualizar el reconocimiento con el nuevo id_imagen
                    cur.execute("""
                        UPDATE reconocimientos
                        SET id_imagen = %s
                        WHERE id_reconocimiento = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_reconocimiento, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Actualizar los datos del reconocimiento
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE reconocimientos
            SET tipo = %s, descripcion = %s, institucion = %s, tipo_institucion = %s, fecha = %s
            WHERE id_reconocimiento = %s AND id_usuario = %s
        """, (tipo, descripcion, institucion, tipo_institucion, fecha, id_reconocimiento, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Reconocimiento actualizado correctamente', 'success')
        return redirect(url_for('reconocimientos'))

    # Prellenar el formulario con los datos actuales
    if request.method == 'GET':
        form.tipo.data = reconocimiento['tipo']
        form.tipo_institucion.data = reconocimiento['tipo_institucion']
        form.descripcion.data = reconocimiento['descripcion']
        form.institucion.data = reconocimiento['institucion']
        form.fecha.data = reconocimiento['fecha']

    return render_template('editar_reconocimiento.html', reconocimiento=reconocimiento, form=form)

# --- RUTA PARA ELIMINAR UN RECONOCIMIENTO ---
@app.route('/eliminar_reconocimiento/<int:id_reconocimiento>', methods=['POST'])
@login_required
def eliminar_reconocimiento(id_reconocimiento):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM reconocimientos
        WHERE id_reconocimiento = %s AND id_usuario = %s
    """, (id_reconocimiento, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar el archivo físico del servidor
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()
        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
            # Eliminar la imagen de la tabla imagenesadjuntas
            cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
            db.connection.commit()

    # Eliminar el reconocimiento
    cur.execute("DELETE FROM reconocimientos WHERE id_reconocimiento = %s AND id_usuario = %s", (id_reconocimiento, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Reconocimiento eliminado correctamente', 'success')
    return redirect(url_for('reconocimientos'))

# --- RUTA PARA AGREGAR Y VISUALIZAR SOFTWARE ESPECIALIZADO ---
@app.route('/softwareespecializado', methods=['GET', 'POST'])
@login_required
def softwareespecializado():
    form = SoftwareEspecializadoForm()
    if form.validate_on_submit():
        nombre_curso = form.nombre_curso.data
        modalidad = form.modalidad.data
        horas = form.horas.data
        institucion = form.institucion.data
        nombre_institucion = form.nombre_institucion.data.strip() if form.nombre_institucion.data else None
        top_1000 = int(form.top_1000.data)
        fecha = form.fecha.data

        # Manejo de archivos (imagen o PDF)
        archivo = form.archivo.data
        id_imagen = None
        if archivo:
            if allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                archivo.save(file_path)

                # Determinar el tipo de archivo (imagen o PDF)
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).', 'danger')
                    return redirect(request.url)

                # Insertar el archivo y obtener su id_imagen
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, nombre_curso, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.', 'danger')
                return redirect(request.url)

        # Insertar el software especializado, incluyendo 'nombre_institucion' y 'top_1000'
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            INSERT INTO softwareespecializado 
            (id_usuario, nombre_curso, modalidad, horas, institucion, nombre_institucion, top_1000, fecha, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, nombre_curso, modalidad, horas, institucion, nombre_institucion, top_1000, fecha, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Software especializado agregado correctamente', 'success')
        return redirect(url_for('softwareespecializado'))

    # Obtener los registros de software especializado del usuario actual
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT se.id_software, se.nombre_curso, se.modalidad, se.horas, se.institucion, se.nombre_institucion, se.top_1000, se.fecha,
               ia.ruta_imagen, ia.categoria
        FROM softwareespecializado se
        LEFT JOIN imagenesadjuntas ia ON se.id_imagen = ia.id_imagen
        WHERE se.id_usuario = %s
    """, [current_user.id])
    softwareespecializados = cur.fetchall()
    cur.close()

    return render_template('softwareespecializado.html', softwareespecializados=softwareespecializados, form=form)

@app.route('/editar_softwareespecializado/<int:id_software>', methods=['GET', 'POST'])
@login_required
def editar_softwareespecializado(id_software):
    form = SoftwareEspecializadoForm()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los datos actuales del software especializado
    cur.execute("""
        SELECT se.id_software, se.nombre_curso, se.modalidad, se.horas, se.institucion, se.nombre_institucion, se.top_1000, se.fecha,
               ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM softwareespecializado se
        LEFT JOIN imagenesadjuntas ia ON se.id_imagen = ia.id_imagen
        WHERE se.id_software = %s AND se.id_usuario = %s
    """, (id_software, current_user.id))
    software = cur.fetchone()
    cur.close()

    if not software:
        flash('Software especializado no encontrado', 'danger')
        return redirect(url_for('softwareespecializado'))

    if form.validate_on_submit():
        nombre_curso = form.nombre_curso.data
        modalidad = form.modalidad.data
        horas = form.horas.data
        institucion = form.institucion.data
        nombre_institucion = form.nombre_institucion.data.strip() if form.nombre_institucion.data else None
        top_1000 = int(form.top_1000.data)
        fecha = form.fecha.data
        archivo = form.archivo.data
        id_imagen_actual = software['id_imagen']

        # Manejo del archivo adjunto (igual que antes)
        # ... (código para manejar el archivo) ...

        # Actualizar los datos del software especializado
        cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            UPDATE softwareespecializado 
            SET nombre_curso = %s, modalidad = %s, horas = %s, institucion = %s, nombre_institucion = %s, top_1000 = %s, fecha = %s
            WHERE id_software = %s AND id_usuario = %s
        """, (nombre_curso, modalidad, horas, institucion, nombre_institucion, top_1000, fecha, id_software, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Software especializado actualizado correctamente', 'success')
        return redirect(url_for('softwareespecializado'))

    # Prellenar el formulario con los datos actuales si es una solicitud GET
    if request.method == 'GET':
        form.nombre_curso.data = software['nombre_curso']
        form.modalidad.data = software['modalidad']
        form.horas.data = software['horas']
        form.institucion.data = software['institucion']
        form.nombre_institucion.data = software['nombre_institucion']
        form.top_1000.data = bool(software['top_1000'])
        form.fecha.data = software['fecha']

    return render_template('editar_softwareespecializado.html', software=software, form=form)


@app.route('/eliminar_softwareespecializado/<int:id_software>', methods=['POST'])
@login_required
def eliminar_softwareespecializado(id_software):
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM softwareespecializado 
        WHERE id_software = %s AND id_usuario = %s
    """, (id_software, current_user.id))
    result = cur.fetchone()

    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar el archivo físico del servidor
        cur.execute("""
            SELECT ruta_imagen FROM imagenesadjuntas 
            WHERE id_imagen = %s AND id_usuario = %s
        """, (id_imagen, current_user.id))
        imagen = cur.fetchone()
        if imagen:
            ruta_imagen = imagen['ruta_imagen']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], ruta_imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))

    # Eliminar el registro de software especializado
    cur.execute("DELETE FROM softwareespecializado WHERE id_software = %s AND id_usuario = %s", (id_software, current_user.id))
    db.connection.commit()
    cur.close()

    flash('Software especializado eliminado correctamente', 'success')
    return redirect(url_for('softwareespecializado'))

# --- NUEVA RUTA PARA TUTORÍAS ---

@app.route('/tutorias', methods=['GET', 'POST'])
@login_required
def tutorias():
    form = TutoriaForm()
    if form.validate_on_submit():
        descripcion = form.descripcion.data
        anio = form.anio.data

        # Manejo de archivos (imagen o PDF)
        file = form.archivo.data
        id_imagen = None
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)

                # Determinar el tipo de archivo (imagen o PDF)
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).')
                    return redirect(request.url)

                cur = db.connection.cursor()
                # Insertar el archivo y obtener su id_imagen
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen = cur.lastrowid
                cur.close()
            else:
                flash('Archivo no permitido.')
                return redirect(request.url)

        # Insertar la tutoría
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO tutorias (id_usuario, descripcion, anio, id_imagen)
            VALUES (%s, %s, %s, %s)
        """, (current_user.id, descripcion, anio, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Tutoría agregada correctamente')
        return redirect(url_for('tutorias'))

    # Obtener las tutorías del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT t.id_tutoria, t.descripcion, t.anio, 
               ia.ruta_imagen, ia.categoria
        FROM tutorias t
        LEFT JOIN imagenesadjuntas ia ON t.id_imagen = ia.id_imagen
        WHERE t.id_usuario = %s
    """, [current_user.id])
    tutorias = cur.fetchall()
    cur.close()

    return render_template('tutorias.html', tutorias=tutorias, form=form)

@app.route('/editar_tutoria/<int:id_tutoria>', methods=['GET', 'POST'])
@login_required
def editar_tutoria(id_tutoria):
    form = TutoriaForm()
    cur = db.connection.cursor()

    # Updated SELECT statement to include id_imagen
    cur.execute("""
        SELECT t.id_tutoria, t.descripcion, t.anio, 
               ia.id_imagen, ia.ruta_imagen, ia.categoria
        FROM tutorias t
        LEFT JOIN imagenesadjuntas ia ON t.id_imagen = ia.id_imagen
        WHERE t.id_tutoria = %s AND t.id_usuario = %s
    """, (id_tutoria, current_user.id))
    tutoria = cur.fetchone()
    cur.close()

    if not tutoria:
        flash('Tutoría no encontrada')
        return redirect(url_for('tutorias'))

    if form.validate_on_submit():
        descripcion = form.descripcion.data
        anio = form.anio.data
        file = form.archivo.data
        id_imagen_actual = tutoria[3]  # ia.id_imagen (integer)

        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)

                # Determine file type
                file_extension = filename.rsplit('.', 1)[1].lower()
                if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                    categoria = 'imagen'
                elif file_extension == 'pdf':
                    categoria = 'pdf'
                else:
                    flash('Debe seleccionar un archivo válido (imagen o PDF).')
                    return redirect(request.url)

                cur = db.connection.cursor()
                if id_imagen_actual:
                    # Update existing imagenesadjuntas row
                    cur.execute("""
                        UPDATE imagenesadjuntas 
                        SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                        WHERE id_imagen = %s AND id_usuario = %s
                    """, (unique_filename, categoria, descripcion, id_imagen_actual, current_user.id))
                else:
                    # Insert new imagenesadjuntas row
                    cur.execute("""
                        INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                        VALUES (%s, %s, %s, %s)
                    """, (current_user.id, categoria, descripcion, unique_filename))
                    db.connection.commit()
                    id_imagen_nueva = cur.lastrowid

                    # Update the tutoria with the new id_imagen
                    cur.execute("""
                        UPDATE tutorias 
                        SET id_imagen = %s 
                        WHERE id_tutoria = %s AND id_usuario = %s
                    """, (id_imagen_nueva, id_tutoria, current_user.id))
                db.connection.commit()
                cur.close()
            else:
                flash('Archivo no permitido.')
                return redirect(request.url)

        # Update the tutoria details
        cur = db.connection.cursor()
        cur.execute("""
            UPDATE tutorias 
            SET descripcion = %s, anio = %s
            WHERE id_tutoria = %s AND id_usuario = %s
        """, (descripcion, anio, id_tutoria, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Tutoría actualizada correctamente')
        return redirect(url_for('tutorias'))

    # Pre-fill the form with existing data on GET request
    if request.method == 'GET':
        form.descripcion.data = tutoria[1]
        form.anio.data = tutoria[2]

    return render_template('editar_tutoria.html', tutoria=tutoria, form=form)


# Ruta para eliminar una tutoría
@app.route('/eliminar_tutoria/<int:id_tutoria>', methods=['POST'])
@login_required
def eliminar_tutoria(id_tutoria):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM tutorias 
        WHERE id_tutoria = %s AND id_usuario = %s
    """, (id_tutoria, current_user.id))
    result = cur.fetchone()
    if result and result[0]:
        id_imagen = result[0]
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar la tutoría
    cur.execute("DELETE FROM tutorias WHERE id_tutoria = %s AND id_usuario = %s", (id_tutoria, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Tutoría eliminada correctamente')
    return redirect(url_for('tutorias'))

# Ruta para que el administrador vea los datos del personal
@app.route('/admin/ver_datos_personal', defaults={'page': 1})
@app.route('/admin/ver_datos_personal/page/<int:page>')
@login_required
def ver_datos_personal(page):
    # Verificar si el usuario es administrador
    if current_user.role != 'Administrador':
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('home'))

    # Definir el número de resultados por página
    resultados_por_pagina = 10

    try:
        cur = db.connection.cursor()
        # Obtener el total de usuarios para la paginación
        cur.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cur.fetchone()[0]

        # Calcular el número total de páginas
        total_paginas = (total_usuarios // resultados_por_pagina) + (1 if total_usuarios % resultados_por_pagina > 0 else 0)

        # Verificar si la página solicitada existe
        if page < 1 or page > total_paginas:
            flash('Página no válida', 'error')
            return redirect(url_for('ver_datos_personal'))

        # Calcular el offset
        offset = (page - 1) * resultados_por_pagina

        # Obtener los datos de los usuarios con paginación, incluyendo el código de la comuna
        cur.execute(f"""
            SELECT 
                usuarios.id_usuario, usuarios.usuario, usuarios.rol,
                datospersonales.nombres, 
                datospersonales.apellido_paterno, 
                datospersonales.apellido_materno,
                datospersonales.dni, 
                datospersonales.correo_personal, 
                datospersonales.movil, 
                datospersonales.codigo
            FROM usuarios
            LEFT JOIN datospersonales ON usuarios.id_usuario = datospersonales.id_usuario
            LIMIT %s OFFSET %s
        """, (resultados_por_pagina, offset))
        usuarios = cur.fetchall()
        cur.close()

    except Exception as e:
        flash('Ocurrió un error al obtener los datos del personal: {}'.format(str(e)), 'error')
        return redirect(url_for('home'))

    return render_template('admin_ver_datos_personal.html', 
                           usuarios=usuarios, 
                           page=page, 
                           total_paginas=total_paginas)

@app.route('/personal_details/<int:user_id>')
@login_required
def ver_detalles_personales(user_id):
    # Verificar si el usuario es administrador
    if current_user.role != 'Administrador':
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('home'))

    try:
        cur = db.connection.cursor()
        # Fetch comprehensive personal details for the specific user
        cur.execute("""
            SELECT 
                dp.id_datos, dp.id_usuario, 
                dp.apellido_paterno, dp.apellido_materno, dp.nombres,
                dp.fecha_nacimiento, 
                dp.lugar_nacimiento_departamento, 
                dp.lugar_nacimiento_provincia, 
                dp.lugar_nacimiento_distrito,
                dp.dni, dp.carne_extranjeria, 
                dp.numero_colegiatura, dp.numero_ruc,
                dp.codigo, dp.condicion, 
                dp.categoria, dp.dedicacion,
                dp.telefono_fijo, dp.movil,
                dp.correo_personal, dp.correo_institucional,
                dp.domicilio_actual, dp.referencia,
                u.usuario, u.rol
            FROM datospersonales dp
            JOIN usuarios u ON dp.id_usuario = u.id_usuario
            WHERE dp.id_usuario = %s
        """, (user_id,))
        
        detalles = cur.fetchone()
        cur.close()

        if not detalles:
            flash('No se encontraron detalles para este usuario', 'error')
            return redirect(url_for('ver_datos_personal'))

        return render_template('detalles_personales.html', detalles=detalles)

    except Exception as e:
        flash(f'Error al obtener detalles personales: {str(e)}', 'error')
        return redirect(url_for('ver_datos_personal'))


# --- FIN DE NUEVAS RUTAS ---

# Manejo de errores y configuración final
if __name__ == '__main__':
        app.config.from_object(config['development'])
        csrf.init_app(app)
        app.run()