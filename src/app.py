# src/app.py
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import time
import bcrypt

from config import config

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

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
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

# --- NUEVAS RUTAS ---

# Ruta para editar datos personales
@app.route('/datos_personales', methods=['GET', 'POST'])
@login_required
def datos_personales():
    if request.method == 'POST':
        # Capturar datos del formulario
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        nombres = request.form['nombres']
        fecha_nacimiento = request.form['fecha_nacimiento']
        lugar_nacimiento_departamento = request.form['lugar_nacimiento_departamento']
        lugar_nacimiento_provincia = request.form['lugar_nacimiento_provincia']
        lugar_nacimiento_distrito = request.form['lugar_nacimiento_distrito']
        dni = request.form['dni']
        carne_extranjeria = request.form.get('carne_extranjeria', '')  # Campo opcional
        numero_colegiatura = request.form.get('numero_colegiatura', '')  # Campo opcional
        numero_ruc = request.form.get('numero_ruc', '')  # Campo opcional
        codigo = request.form['codigo']
        condicion = request.form['condicion']
        categoria = request.form['categoria']
        dedicacion = request.form['dedicacion']
        telefono_fijo = request.form['telefono_fijo']
        movil = request.form['movil']
        correo_personal = request.form['correo_personal']
        correo_institucional = request.form['correo_institucional']
        domicilio_actual = request.form['domicilio_actual']
        referencia = request.form.get('referencia', '')  # Campo opcional

        # Verificar si ya existen datos personales para el usuario
        cur = db.connection.cursor()
        cur.execute("SELECT id_datos FROM datospersonales WHERE id_usuario = %s", [current_user.id])
        data = cur.fetchone()

        if data:
            # Actualizar datos existentes
            cur.execute(""" 
                UPDATE datospersonales SET 
                    apellido_paterno=%s, 
                    apellido_materno=%s, 
                    nombres=%s, 
                    fecha_nacimiento=%s,
                    lugar_nacimiento_departamento=%s, 
                    lugar_nacimiento_provincia=%s, 
                    lugar_nacimiento_distrito=%s, 
                    dni=%s,
                    carne_extranjeria=%s, 
                    numero_colegiatura=%s, 
                    numero_ruc=%s, 
                    codigo=%s, 
                    condicion=%s, 
                    categoria=%s,
                    dedicacion=%s, 
                    telefono_fijo=%s, 
                    movil=%s, 
                    correo_personal=%s, 
                    correo_institucional=%s,
                    domicilio_actual=%s, 
                    referencia=%s 
                WHERE id_usuario=%s
            """, (apellido_paterno, apellido_materno, nombres, fecha_nacimiento,
                  lugar_nacimiento_departamento, lugar_nacimiento_provincia, lugar_nacimiento_distrito, dni,
                  carne_extranjeria, numero_colegiatura, numero_ruc, codigo, condicion, categoria,
                  dedicacion, telefono_fijo, movil, correo_personal, correo_institucional,
                  domicilio_actual, referencia, current_user.id))
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
                    carne_extranjeria, 
                    numero_colegiatura, 
                    numero_ruc, 
                    codigo, 
                    condicion, 
                    categoria,
                    dedicacion, 
                    telefono_fijo, 
                    movil, 
                    correo_personal, 
                    correo_institucional,
                    domicilio_actual, 
                    referencia
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (current_user.id, apellido_paterno, apellido_materno, nombres, fecha_nacimiento,
                  lugar_nacimiento_departamento, lugar_nacimiento_provincia, lugar_nacimiento_distrito, dni,
                  carne_extranjeria, numero_colegiatura, numero_ruc, codigo, condicion, categoria,
                  dedicacion, telefono_fijo, movil, correo_personal, correo_institucional,
                  domicilio_actual, referencia))

        db.connection.commit()
        cur.close()
        flash('Datos personales actualizados correctamente')
        return redirect(url_for('home'))

    # Obtener datos personales actuales
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM datospersonales WHERE id_usuario = %s", [current_user.id])
    data = cur.fetchone()
    cur.close()

    # Preparar los datos para ser renderizados en el formulario
    data_dict = {
        'apellido_paterno': data[2] if data else '',
        'apellido_materno': data[3] if data else '',
        'nombres': data[4] if data else '',
        'fecha_nacimiento': data[5] if data else '',
        'lugar_nacimiento_departamento': data[6] if data else '',
        'lugar_nacimiento_provincia': data[7] if data else '',
        'lugar_nacimiento_distrito': data[8] if data else '',
        'dni': data[9] if data else '',
        'carne_extranjeria': data[10] if data else '',
        'numero_colegiatura': data[11] if data else '',
        'numero_ruc': data[12] if data else '',
        'codigo': data[13] if data else '',
        'condicion': data[14] if data else '',
        'categoria': data[15] if data else '',
        'dedicacion': data[16] if data else '',
        'telefono_fijo': data[17] if data else '',
        'movil': data[18] if data else '',
        'correo_personal': data[19] if data else '',
        'correo_institucional': data[20] if data else '',
        'domicilio_actual': data[21] if data else '',
        'referencia': data[22] if data else ''
    }

    return render_template('datos_personales.html', data=data_dict)




# Ruta para listar y agregar grados y títulos
# Ruta para editar un grado/título
# Ruta para agregar un nuevo grado/título con imagen
# Ruta para servir las imágenes

@app.route('/grados_titulos', methods=['GET', 'POST'])
@login_required
def grados_titulos():
    if request.method == 'POST':
        # Capturar los datos del formulario
        titulo = request.form['titulo']
        tipo = request.form['tipo']
        universidad = request.form['universidad']
        pais = request.form['pais']
        fecha_expedicion = request.form['fecha_expedicion']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo (imagen o PDF)
            file_extension = filename.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            cur = db.connection.cursor()
            # Insertar el archivo y obtener su id_archivo
            cur.execute("""
                INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                VALUES (%s, %s, %s, %s)
            """, (current_user.id, categoria, titulo, unique_filename))
            db.connection.commit()
            id_imagen = cur.lastrowid  # Obtener el id de la imagen o archivo insertado

            # Insertar el grado/título con id_imagen
            cur.execute("""
                INSERT INTO gradostitulos (id_usuario, titulo, tipo, universidad, pais, fecha_expedicion, id_imagen)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (current_user.id, titulo, tipo, universidad, pais, fecha_expedicion, id_imagen))
            db.connection.commit()
            cur.close()

            flash('Grado/Título y el archivo han sido agregados correctamente')
            return redirect(url_for('grados_titulos'))
        else:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

    # Obtener los grados y títulos del usuario actual junto con sus imágenes o archivos
    cur = db.connection.cursor()
    cur.execute("""
        SELECT gradostitulos.*, imagenesadjuntas.ruta_imagen, imagenesadjuntas.categoria
        FROM gradostitulos
        LEFT JOIN imagenesadjuntas ON gradostitulos.id_imagen = imagenesadjuntas.id_imagen
        WHERE gradostitulos.id_usuario = %s
    """, [current_user.id])
    titulos = cur.fetchall()
    cur.close()

    return render_template('grados_titulos.html', titulos=titulos)


@app.route('/editar_grado/<int:id_grado>', methods=['GET', 'POST'])
@login_required
def editar_grado(id_grado):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        titulo = request.form['titulo']
        tipo = request.form['tipo']
        universidad = request.form['universidad']
        pais = request.form['pais']
        fecha_expedicion = request.form['fecha_expedicion']
        file = request.files.get('archivo')  # Ahora aceptamos tanto imágenes como PDFs
        
        # Obtener el id_imagen actual del grado/título
        cur.execute("""
            SELECT id_imagen FROM gradostitulos 
            WHERE id_grado = %s AND id_usuario = %s
        """, (id_grado, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None
        
        # Procesar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Generar un nombre único para el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Detectar si el archivo es una imagen o un PDF
            file_extension = filename.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Archivo no válido. Solo se permiten imágenes y PDFs.')
                return redirect(request.url)
            
            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, titulo, id_imagen_actual))
            else:
                # Insertar un nuevo archivo y actualizar el grado/título
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, titulo, unique_filename))
                db.connection.commit()
                id_imagen_nueva = cur.lastrowid
                
                # Actualizar el grado/título con el nuevo id_imagen
                cur.execute("""
                    UPDATE gradostitulos 
                    SET id_imagen = %s 
                    WHERE id_grado = %s AND id_usuario = %s
                """, (id_imagen_nueva, id_grado, current_user.id))
        else:
            # Si no se sube un nuevo archivo, actualizar categoría y descripción si es necesario
            if id_imagen_actual:
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET categoria = %s, descripcion = %s
                    WHERE id_imagen = %s
                """, (tipo, titulo, id_imagen_actual))
        
        # Actualizar los datos del grado/título
        cur.execute("""
            UPDATE gradostitulos 
            SET titulo = %s, tipo = %s, universidad = %s, pais = %s, fecha_expedicion = %s
            WHERE id_grado = %s AND id_usuario = %s
        """, (titulo, tipo, universidad, pais, fecha_expedicion, id_grado, current_user.id))
        
        db.connection.commit()
        cur.close()
        
        flash('Grado/Título actualizado correctamente')
        return redirect(url_for('grados_titulos'))
    
    # Obtener los datos actuales del grado/título
    cur.execute("""
        SELECT gradostitulos.*, imagenesadjuntas.ruta_imagen
        FROM gradostitulos
        LEFT JOIN imagenesadjuntas ON gradostitulos.id_imagen = imagenesadjuntas.id_imagen
        WHERE gradostitulos.id_grado = %s AND gradostitulos.id_usuario = %s
    """, (id_grado, current_user.id))
    titulo = cur.fetchone()
    cur.close()
    
    if titulo:
        return render_template('editar_grado.html', titulo=titulo, imagen_actual=titulo[-1])  # titulo[-1] es ruta_imagen
    else:
        flash('Grado/Título no encontrado')
        return redirect(url_for('grados_titulos'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Ruta del archivo: {file_path}")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Ruta para eliminar un grado/título
@app.route('/eliminar_grado/<int:id_grado>', methods=['POST'])
@login_required
def eliminar_grado(id_grado):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM gradostitulos WHERE id_grado = %s AND id_usuario = %s", (id_grado, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Grado/Título eliminado correctamente')
    return redirect(url_for('grados_titulos'))


# Ruta para manejar actividades de proyección social
@app.route('/actividades_proyeccion_social', methods=['GET', 'POST'])
@login_required
def actividades_proyeccion_social():
    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        evento = request.form['evento']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar la actividad
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO actividadesproyeccionsocial (id_usuario, tipo, evento, descripcion, fecha, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, evento, descripcion, fecha, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Actividad de Proyección Social agregada correctamente')
        return redirect(url_for('actividades_proyeccion_social'))

    # Obtener las actividades del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT aps.id_actividad, aps.tipo, aps.evento, aps.descripcion, aps.fecha, aps.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM actividadesproyeccionsocial aps
        LEFT JOIN imagenesadjuntas ia ON aps.id_imagen = ia.id_imagen
        WHERE aps.id_usuario = %s
    """, [current_user.id])
    actividades = cur.fetchall()
    cur.close()

    return render_template('actividades_proyeccion_social.html', actividades=actividades)

# Ruta para editar una actividad de proyección social
@app.route('/editar_actividad/<int:id_actividad>', methods=['GET', 'POST'])
@login_required
def editar_actividad(id_actividad):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        evento = request.form['evento']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM actividadesproyeccionsocial 
            WHERE id_actividad = %s AND id_usuario = %s
        """, (id_actividad, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, descripcion, id_imagen_actual))
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

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos de la actividad
        cur.execute("""
            UPDATE actividadesproyeccionsocial 
            SET tipo = %s, evento = %s, descripcion = %s, fecha = %s, puntaje = %s
            WHERE id_actividad = %s AND id_usuario = %s
        """, (tipo, evento, descripcion, fecha, puntaje, id_actividad, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Actividad de Proyección Social actualizada correctamente')
        return redirect(url_for('actividades_proyeccion_social'))

    # Obtener los datos actuales de la actividad
    cur.execute("""
        SELECT aps.id_actividad, aps.tipo, aps.evento, aps.descripcion, aps.fecha, aps.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM actividadesproyeccionsocial aps
        LEFT JOIN imagenesadjuntas ia ON aps.id_imagen = ia.id_imagen
        WHERE aps.id_actividad = %s AND aps.id_usuario = %s
    """, (id_actividad, current_user.id))
    actividad = cur.fetchone()
    cur.close()

    if actividad:
        return render_template('editar_actividad.html', actividad=actividad)
    else:
        flash('Actividad no encontrada')
        return redirect(url_for('actividades_proyeccion_social'))

# Ruta para eliminar una actividad de proyección social
@app.route('/eliminar_actividad/<int:id_actividad>', methods=['POST'])
@login_required
def eliminar_actividad(id_actividad):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM actividadesproyeccionsocial 
        WHERE id_actividad = %s AND id_usuario = %s
    """, (id_actividad, current_user.id))
    result = cur.fetchone()
    if result and result[0]:
        id_imagen = result[0]
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar la actividad
    cur.execute("DELETE FROM actividadesproyeccionsocial WHERE id_actividad = %s AND id_usuario = %s", (id_actividad, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Actividad de Proyección Social eliminada correctamente')
    return redirect(url_for('actividades_proyeccion_social'))

# Nueva Ruta para manejar Actualizaciones y Capacitaciones
@app.route('/actualizaciones_capacitaciones', methods=['GET', 'POST'])
@login_required
def actualizaciones_capacitaciones():
    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        horas = request.form['horas']
        creditos = request.form['creditos']
        semestres_concluidos = request.form['semestres_concluidos']
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar la actualización/capacitación
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO actualizacionescapacitaciones (id_usuario, tipo, descripcion, horas, creditos, semestres_concluidos, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, descripcion, horas, creditos, semestres_concluidos, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Actualización/Capacitación agregada correctamente')
        return redirect(url_for('actualizaciones_capacitaciones'))

    # Obtener las actualizaciones y capacitaciones del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT ac.id_capacitacion, ac.tipo, ac.descripcion, ac.horas, ac.creditos, ac.semestres_concluidos, 
               ac.puntaje, ia.ruta_imagen, ia.categoria
        FROM actualizacionescapacitaciones ac
        LEFT JOIN imagenesadjuntas ia ON ac.id_imagen = ia.id_imagen
        WHERE ac.id_usuario = %s
    """, [current_user.id])
    actualizaciones = cur.fetchall()
    cur.close()

    return render_template('actualizaciones_capacitaciones.html', actualizaciones=actualizaciones)

# Ruta para editar una Actualización/Capacitación
@app.route('/editar_actualizacion/<int:id_capacitacion>', methods=['GET', 'POST'])
@login_required
def editar_actualizacion(id_capacitacion):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        horas = request.form['horas']
        creditos = request.form['creditos']
        semestres_concluidos = request.form['semestres_concluidos']
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM actualizacionescapacitaciones 
            WHERE id_capacitacion = %s AND id_usuario = %s
        """, (id_capacitacion, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, descripcion, id_imagen_actual))
            else:
                # Insertar un nuevo archivo
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen_nueva = cur.lastrowid

                # Actualizar la actualización/capacitación con el nuevo id_imagen
                cur.execute("""
                    UPDATE actualizacionescapacitaciones 
                    SET id_imagen = %s 
                    WHERE id_capacitacion = %s AND id_usuario = %s
                """, (id_imagen_nueva, id_capacitacion, current_user.id))

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos de la actualización/capacitación
        cur.execute("""
            UPDATE actualizacionescapacitaciones 
            SET tipo = %s, descripcion = %s, horas = %s, creditos = %s, semestres_concluidos = %s, puntaje = %s
            WHERE id_capacitacion = %s AND id_usuario = %s
        """, (tipo, descripcion, horas, creditos, semestres_concluidos, puntaje, id_capacitacion, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Actualización/Capacitación actualizada correctamente')
        return redirect(url_for('actualizaciones_capacitaciones'))

    # Obtener los datos actuales de la actualización/capacitación
    cur.execute("""
        SELECT ac.id_capacitacion, ac.tipo, ac.descripcion, ac.horas, ac.creditos, ac.semestres_concluidos, 
               ac.puntaje, ia.ruta_imagen, ia.categoria
        FROM actualizacionescapacitaciones ac
        LEFT JOIN imagenesadjuntas ia ON ac.id_imagen = ia.id_imagen
        WHERE ac.id_capacitacion = %s AND ac.id_usuario = %s
    """, (id_capacitacion, current_user.id))
    actualizacion = cur.fetchone()
    cur.close()

    if actualizacion:
        return render_template('editar_actualizacion_capacitacion.html', actualizacion=actualizacion)
    else:
        flash('Actualización/Capacitación no encontrada')
        return redirect(url_for('actualizaciones_capacitaciones'))

# Ruta para eliminar una Actualización/Capacitación
@app.route('/eliminar_actualizacion/<int:id_capacitacion>', methods=['POST'])
@login_required
def eliminar_actualizacion(id_capacitacion):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM actualizacionescapacitaciones 
        WHERE id_capacitacion = %s AND id_usuario = %s
    """, (id_capacitacion, current_user.id))
    result = cur.fetchone()
    if result and result[0]:
        id_imagen = result[0]
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar la actualización/capacitación
    cur.execute("DELETE FROM actualizacionescapacitaciones WHERE id_capacitacion = %s AND id_usuario = %s", (id_capacitacion, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Actualización/Capacitación eliminada correctamente')
    return redirect(url_for('actualizaciones_capacitaciones'))

# Ruta para listar y agregar cargos directivos
@app.route('/cargos_directivos', methods=['GET', 'POST'])
@login_required
def cargos_directivos():
    if request.method == 'POST':
        # Capturar datos del formulario
        cargo = request.form['cargo']
        anios = request.form['anios']
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
            """, (current_user.id, categoria, cargo, unique_filename))
            db.connection.commit()
            id_imagen = cur.lastrowid
            cur.close()
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar el cargo directivo
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO cargosdirectivos (id_usuario, cargo, anios, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s)
        """, (current_user.id, cargo, anios, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Cargo Directivo agregado correctamente')
        return redirect(url_for('cargos_directivos'))

    # Obtener los cargos directivos del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT cd.id_cargo, cd.cargo, cd.anios, cd.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM cargosdirectivos cd
        LEFT JOIN imagenesadjuntas ia ON cd.id_imagen = ia.id_imagen
        WHERE cd.id_usuario = %s
    """, [current_user.id])
    cargos = cur.fetchall()
    cur.close()

    return render_template('cargos_directivos.html', cargos=cargos)

# Ruta para editar un cargo directivo
@app.route('/editar_cargo/<int:id_cargo>', methods=['GET', 'POST'])
@login_required
def editar_cargo(id_cargo):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        cargo = request.form['cargo']
        anios = request.form['anios']
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM cargosdirectivos 
            WHERE id_cargo = %s AND id_usuario = %s
        """, (id_cargo, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, cargo, id_imagen_actual))
            else:
                # Insertar un nuevo archivo
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, cargo, unique_filename))
                db.connection.commit()
                id_imagen_nueva = cur.lastrowid

                # Actualizar el cargo directivo con el nuevo id_imagen
                cur.execute("""
                    UPDATE cargosdirectivos 
                    SET id_imagen = %s 
                    WHERE id_cargo = %s AND id_usuario = %s
                """, (id_imagen_nueva, id_cargo, current_user.id))

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos del cargo directivo
        cur.execute("""
            UPDATE cargosdirectivos 
            SET cargo = %s, anios = %s, puntaje = %s
            WHERE id_cargo = %s AND id_usuario = %s
        """, (cargo, anios, puntaje, id_cargo, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Cargo Directivo actualizado correctamente')
        return redirect(url_for('cargos_directivos'))

    # Obtener los datos actuales del cargo directivo
    cur.execute("""
        SELECT cd.id_cargo, cd.cargo, cd.anios, cd.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM cargosdirectivos cd
        LEFT JOIN imagenesadjuntas ia ON cd.id_imagen = ia.id_imagen
        WHERE cd.id_cargo = %s AND cd.id_usuario = %s
    """, (id_cargo, current_user.id))
    cargo_directivo = cur.fetchone()
    cur.close()

    if cargo_directivo:
        return render_template('editar_cargo_directivo.html', cargo=cargo_directivo)
    else:
        flash('Cargo Directivo no encontrado')
        return redirect(url_for('cargos_directivos'))

# Ruta para eliminar un cargo directivo
@app.route('/eliminar_cargo/<int:id_cargo>', methods=['POST'])
@login_required
def eliminar_cargo(id_cargo):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM cargosdirectivos 
        WHERE id_cargo = %s AND id_usuario = %s
    """, (id_cargo, current_user.id))
    result = cur.fetchone()
    if result and result[0]:
        id_imagen = result[0]
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar el cargo directivo
    cur.execute("DELETE FROM cargosdirectivos WHERE id_cargo = %s AND id_usuario = %s", (id_cargo, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Cargo Directivo eliminado correctamente')
    return redirect(url_for('cargos_directivos'))

# Ruta para listar y agregar experiencia docente
@app.route('/experiencia_docente', methods=['GET', 'POST'])
@login_required
def experiencia_docente():
    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        anios = request.form['anios']
        cursos = request.form['cursos']
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar la experiencia docente
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO experienciadocente (id_usuario, tipo, descripcion, anios, cursos, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, descripcion, anios, cursos, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Experiencia Docente agregada correctamente')
        return redirect(url_for('experiencia_docente'))

    # Obtener las experiencias docentes del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT ed.id_experiencia, ed.tipo, ed.descripcion, ed.anios, ed.cursos, ed.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM experienciadocente ed
        LEFT JOIN imagenesadjuntas ia ON ed.id_imagen = ia.id_imagen
        WHERE ed.id_usuario = %s
    """, [current_user.id])
    experiencias = cur.fetchall()
    cur.close()

    return render_template('experiencia_docente.html', experiencias=experiencias)

# Ruta para editar una experiencia docente
@app.route('/editar_experiencia/<int:id_experiencia>', methods=['GET', 'POST'])
@login_required
def editar_experiencia(id_experiencia):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        anios = request.form['anios']
        cursos = request.form['cursos']
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM experienciadocente 
            WHERE id_experiencia = %s AND id_usuario = %s
        """, (id_experiencia, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, descripcion, id_imagen_actual))
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

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos de la experiencia docente
        cur.execute("""
            UPDATE experienciadocente 
            SET tipo = %s, descripcion = %s, anios = %s, cursos = %s, puntaje = %s
            WHERE id_experiencia = %s AND id_usuario = %s
        """, (tipo, descripcion, anios, cursos, puntaje, id_experiencia, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Experiencia Docente actualizada correctamente')
        return redirect(url_for('experiencia_docente'))

    # Obtener los datos actuales de la experiencia docente
    cur.execute("""
        SELECT ed.id_experiencia, ed.tipo, ed.descripcion, ed.anios, ed.cursos, ed.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM experienciadocente ed
        LEFT JOIN imagenesadjuntas ia ON ed.id_imagen = ia.id_imagen
        WHERE ed.id_experiencia = %s AND ed.id_usuario = %s
    """, (id_experiencia, current_user.id))
    experiencia = cur.fetchone()
    cur.close()

    if experiencia:
        return render_template('editar_experiencia_docente.html', experiencia=experiencia)
    else:
        flash('Experiencia Docente no encontrada')
        return redirect(url_for('experiencia_docente'))

# Ruta para eliminar una experiencia docente
@app.route('/eliminar_experiencia/<int:id_experiencia>', methods=['POST'])
@login_required
def eliminar_experiencia(id_experiencia):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM experienciadocente 
        WHERE id_experiencia = %s AND id_usuario = %s
    """, (id_experiencia, current_user.id))
    result = cur.fetchone()
    if result and result[0]:
        id_imagen = result[0]
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar la experiencia docente
    cur.execute("DELETE FROM experienciadocente WHERE id_experiencia = %s AND id_usuario = %s", (id_experiencia, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Experiencia Docente eliminada correctamente')
    return redirect(url_for('experiencia_docente'))


# --- NUEVA RUTA PARA IDIOMAS ---

# Ruta para listar y agregar idiomas
@app.route('/idiomas', methods=['GET', 'POST'])
@login_required
def idiomas():
    if request.method == 'POST':
        # Capturar datos del formulario
        idioma = request.form['idioma']
        nivel = request.form['nivel']
        certificado = request.form['certificado']
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
            """, (current_user.id, categoria, idioma, unique_filename))
            db.connection.commit()
            id_imagen = cur.lastrowid
            cur.close()
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar el idioma
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO idiomas (id_usuario, idioma, nivel, certificado, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (current_user.id, idioma, nivel, certificado, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Idioma agregado correctamente')
        return redirect(url_for('idiomas'))

    # Obtener los idiomas del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT i.id_idioma, i.idioma, i.nivel, i.certificado, i.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM idiomas i
        LEFT JOIN imagenesadjuntas ia ON i.id_imagen = ia.id_imagen
        WHERE i.id_usuario = %s
    """, [current_user.id])
    idiomas = cur.fetchall()
    cur.close()

    return render_template('idiomas.html', idiomas=idiomas)

# Ruta para editar un idioma
@app.route('/editar_idioma/<int:id_idioma>', methods=['GET', 'POST'])
@login_required
def editar_idioma(id_idioma):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        idioma = request.form['idioma']
        nivel = request.form['nivel']
        certificado = request.form['certificado']
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM idiomas 
            WHERE id_idioma = %s AND id_usuario = %s
        """, (id_idioma, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, idioma, id_imagen_actual))
            else:
                # Insertar un nuevo archivo
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, idioma, unique_filename))
                db.connection.commit()
                id_imagen_nueva = cur.lastrowid

                # Actualizar el idioma con el nuevo id_imagen
                cur.execute("""
                    UPDATE idiomas 
                    SET id_imagen = %s 
                    WHERE id_idioma = %s AND id_usuario = %s
                """, (id_imagen_nueva, id_idioma, current_user.id))

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos del idioma
        cur.execute("""
            UPDATE idiomas 
            SET idioma = %s, nivel = %s, certificado = %s, puntaje = %s
            WHERE id_idioma = %s AND id_usuario = %s
        """, (idioma, nivel, certificado, puntaje, id_idioma, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Idioma actualizado correctamente')
        return redirect(url_for('idiomas'))

    # Obtener los datos actuales del idioma
    cur.execute("""
        SELECT i.id_idioma, i.idioma, i.nivel, i.certificado, i.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM idiomas i
        LEFT JOIN imagenesadjuntas ia ON i.id_imagen = ia.id_imagen
        WHERE i.id_idioma = %s AND i.id_usuario = %s
    """, (id_idioma, current_user.id))
    idioma_data = cur.fetchone()
    cur.close()

    if idioma_data:
        return render_template('editar_idioma.html', idioma=idioma_data)
    else:
        flash('Idioma no encontrado')
        return redirect(url_for('idiomas'))

# Ruta para eliminar un idioma
@app.route('/eliminar_idioma/<int:id_idioma>', methods=['POST'])
@login_required
def eliminar_idioma(id_idioma):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM idiomas 
        WHERE id_idioma = %s AND id_usuario = %s
    """, (id_idioma, current_user.id))
    result = cur.fetchone()
    if result and result[0]:
        id_imagen = result[0]
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar el idioma
    cur.execute("DELETE FROM idiomas WHERE id_idioma = %s AND id_usuario = %s", (id_idioma, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Idioma eliminado correctamente')
    return redirect(url_for('idiomas'))
# --- NUEVA RUTA PARA INVESTIGACIONES ---

# Ruta para listar y agregar investigaciones
@app.route('/investigaciones', methods=['GET', 'POST'])
@login_required
def investigaciones():
    if request.method == 'POST':
        # Capturar datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
            """, (current_user.id, categoria, titulo, unique_filename))
            db.connection.commit()
            id_imagen = cur.lastrowid
            cur.close()
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar la investigación
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO investigaciones (id_usuario, titulo, descripcion, fecha_inicio, fecha_fin, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, titulo, descripcion, fecha_inicio, fecha_fin, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Investigación agregada correctamente')
        return redirect(url_for('investigaciones'))

    # Obtener las investigaciones del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT inv.id_investigacion, inv.titulo, inv.descripcion, inv.fecha_inicio, inv.fecha_fin, inv.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM investigaciones inv
        LEFT JOIN imagenesadjuntas ia ON inv.id_imagen = ia.id_imagen
        WHERE inv.id_usuario = %s
    """, [current_user.id])
    investigaciones = cur.fetchall()
    cur.close()

    return render_template('investigaciones.html', investigaciones=investigaciones)

# Ruta para editar una investigación
@app.route('/editar_investigacion/<int:id_investigacion>', methods=['GET', 'POST'])
@login_required
def editar_investigacion(id_investigacion):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM investigaciones 
            WHERE id_investigacion = %s AND id_usuario = %s
        """, (id_investigacion, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, titulo, id_imagen_actual))
            else:
                # Insertar un nuevo archivo
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, titulo, unique_filename))
                db.connection.commit()
                id_imagen_nueva = cur.lastrowid

                # Actualizar la investigación con el nuevo id_imagen
                cur.execute("""
                    UPDATE investigaciones 
                    SET id_imagen = %s 
                    WHERE id_investigacion = %s AND id_usuario = %s
                """, (id_imagen_nueva, id_investigacion, current_user.id))

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos de la investigación
        cur.execute("""
            UPDATE investigaciones 
            SET titulo = %s, descripcion = %s, fecha_inicio = %s, fecha_fin = %s, puntaje = %s
            WHERE id_investigacion = %s AND id_usuario = %s
        """, (titulo, descripcion, fecha_inicio, fecha_fin, puntaje, id_investigacion, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Investigación actualizada correctamente')
        return redirect(url_for('investigaciones'))

    # Obtener los datos actuales de la investigación
    cur.execute("""
        SELECT inv.id_investigacion, inv.titulo, inv.descripcion, inv.fecha_inicio, inv.fecha_fin, inv.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM investigaciones inv
        LEFT JOIN imagenesadjuntas ia ON inv.id_imagen = ia.id_imagen
        WHERE inv.id_investigacion = %s AND inv.id_usuario = %s
    """, (id_investigacion, current_user.id))
    investigacion = cur.fetchone()
    cur.close()

    if investigacion:
        return render_template('editar_investigacion.html', investigacion=investigacion)
    else:
        flash('Investigación no encontrada')
        return redirect(url_for('investigaciones'))

# Ruta para eliminar una investigación
@app.route('/eliminar_investigacion/<int:id_investigacion>', methods=['POST'])
@login_required
def eliminar_investigacion(id_investigacion):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM investigaciones 
        WHERE id_investigacion = %s AND id_usuario = %s
    """, (id_investigacion, current_user.id))
    result = cur.fetchone()
    if result and result[0]:
        id_imagen = result[0]
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar la investigación
    cur.execute("DELETE FROM investigaciones WHERE id_investigacion = %s AND id_usuario = %s", (id_investigacion, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Investigación eliminada correctamente')
    return redirect(url_for('investigaciones'))

# --- NUEVA RUTA PARA PARTICIPACIONTESIS ---

# Ruta para listar y agregar participación en tesis
@app.route('/participaciontesis', methods=['GET', 'POST'])
@login_required
def participaciontesis():
    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        nivel = request.form['nivel']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        universidad = request.form['universidad']
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar la participación en tesis
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO participaciontesis (id_usuario, tipo, nivel, descripcion, fecha, universidad, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, nivel, descripcion, fecha, universidad, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Participación en Tesis agregada correctamente')
        return redirect(url_for('participaciontesis'))

    # Obtener las participaciones en tesis del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT pt.id_participaciontesis, pt.tipo, pt.nivel, pt.descripcion, pt.fecha, pt.universidad, pt.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM participaciontesis pt
        LEFT JOIN imagenesadjuntas ia ON pt.id_imagen = ia.id_imagen
        WHERE pt.id_usuario = %s
    """, [current_user.id])
    participaciones = cur.fetchall()
    cur.close()

    return render_template('participaciontesis.html', participaciones=participaciones)

# Ruta para editar una participación en tesis
@app.route('/editar_participaciontesis/<int:id_participaciontesis>', methods=['GET', 'POST'])
@login_required
def editar_participaciontesis(id_participaciontesis):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        nivel = request.form['nivel']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        universidad = request.form['universidad']
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM participaciontesis 
            WHERE id_participaciontesis = %s AND id_usuario = %s
        """, (id_participaciontesis, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, descripcion, id_imagen_actual))
            else:
                # Insertar un nuevo archivo
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen_nueva = cur.lastrowid

                # Actualizar la participación en tesis con el nuevo id_imagen
                cur.execute("""
                    UPDATE participaciontesis 
                    SET id_imagen = %s 
                    WHERE id_participaciontesis = %s AND id_usuario = %s
                """, (id_imagen_nueva, id_participaciontesis, current_user.id))

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos de la participación en tesis
        cur.execute("""
            UPDATE participaciontesis 
            SET tipo = %s, nivel = %s, descripcion = %s, fecha = %s, universidad = %s, puntaje = %s
            WHERE id_participaciontesis = %s AND id_usuario = %s
        """, (tipo, nivel, descripcion, fecha, universidad, puntaje, id_participaciontesis, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Participación en Tesis actualizada correctamente')
        return redirect(url_for('participaciontesis'))

    # Obtener los datos actuales de la participación en tesis
    cur.execute("""
        SELECT pt.id_participaciontesis, pt.tipo, pt.nivel, pt.descripcion, pt.fecha, pt.universidad, pt.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM participaciontesis pt
        LEFT JOIN imagenesadjuntas ia ON pt.id_imagen = ia.id_imagen
        WHERE pt.id_participaciontesis = %s AND pt.id_usuario = %s
    """, (id_participaciontesis, current_user.id))
    participacion = cur.fetchone()
    cur.close()

    if participacion:
        return render_template('editar_participaciontesis.html', participacion=participacion)
    else:
        flash('Participación en Tesis no encontrada')
        return redirect(url_for('participaciontesis'))

# Ruta para eliminar una participación en tesis
@app.route('/eliminar_participaciontesis/<int:id_participaciontesis>', methods=['POST'])
@login_required
def eliminar_participaciontesis(id_participaciontesis):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM participaciontesis 
        WHERE id_participaciontesis = %s AND id_usuario = %s
    """, (id_participaciontesis, current_user.id))
    result = cur.fetchone()
    if result and result[0]:
        id_imagen = result[0]
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar la participación en tesis
    cur.execute("DELETE FROM participaciontesis WHERE id_participaciontesis = %s AND id_usuario = %s", (id_participaciontesis, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Participación en Tesis eliminada correctamente')
    return redirect(url_for('participaciontesis'))

# --- NUEVA RUTA PARA PRODUCCIÓN INTELECTUAL ---

# Ruta para listar y agregar producción intelectual
@app.route('/produccion_intelectual', methods=['GET', 'POST'])
@login_required
def produccion_intelectual():
    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        titulo = request.form['titulo']
        isbn = request.form['isbn']
        deposito_legal = request.form.get('deposito_legal') == 'on'
        fecha_publicacion = request.form['fecha_publicacion']
        autor = request.form.get('autor') == 'on'
        coautor = request.form.get('coautor') == 'on'
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
            """, (current_user.id, categoria, titulo, unique_filename))
            db.connection.commit()
            id_imagen = cur.lastrowid
            cur.close()
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar la producción intelectual
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO produccionintelectual (id_usuario, tipo, titulo, isbn, deposito_legal, fecha_publicacion, autor, coautor, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, titulo, isbn, deposito_legal, fecha_publicacion, autor, coautor, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Producción Intelectual agregada correctamente')
        return redirect(url_for('produccion_intelectual'))

    # Obtener las producciones intelectuales del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT pi.id_produccion, pi.tipo, pi.titulo, pi.isbn, pi.deposito_legal, pi.fecha_publicacion, 
               pi.autor, pi.coautor, pi.puntaje, ia.ruta_imagen, ia.categoria
        FROM produccionintelectual pi
        LEFT JOIN imagenesadjuntas ia ON pi.id_imagen = ia.id_imagen
        WHERE pi.id_usuario = %s
    """, [current_user.id])
    producciones = cur.fetchall()
    cur.close()

    return render_template('produccion_intelectual.html', producciones=producciones)

# Ruta para editar una producción intelectual
@app.route('/editar_produccion/<int:id_produccion>', methods=['GET', 'POST'])
@login_required
def editar_produccion(id_produccion):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        titulo = request.form['titulo']
        isbn = request.form['isbn']
        deposito_legal = request.form.get('deposito_legal') == 'on'
        fecha_publicacion = request.form['fecha_publicacion']
        autor = request.form.get('autor') == 'on'
        coautor = request.form.get('coautor') == 'on'
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM produccionintelectual 
            WHERE id_produccion = %s AND id_usuario = %s
        """, (id_produccion, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, titulo, id_imagen_actual))
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

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos de la producción intelectual
        cur.execute("""
            UPDATE produccionintelectual 
            SET tipo = %s, titulo = %s, isbn = %s, deposito_legal = %s, 
                fecha_publicacion = %s, autor = %s, coautor = %s, puntaje = %s
            WHERE id_produccion = %s AND id_usuario = %s
        """, (tipo, titulo, isbn, deposito_legal, fecha_publicacion, autor, coautor, puntaje, id_produccion, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Producción Intelectual actualizada correctamente')
        return redirect(url_for('produccion_intelectual'))

    # Obtener los datos actuales de la producción intelectual
    cur.execute("""
        SELECT pi.id_produccion, pi.tipo, pi.titulo, pi.isbn, pi.deposito_legal, pi.fecha_publicacion, 
               pi.autor, pi.coautor, pi.puntaje, ia.ruta_imagen, ia.categoria
        FROM produccionintelectual pi
        LEFT JOIN imagenesadjuntas ia ON pi.id_imagen = ia.id_imagen
        WHERE pi.id_produccion = %s AND pi.id_usuario = %s
    """, (id_produccion, current_user.id))
    produccion = cur.fetchone()
    cur.close()

    if produccion:
        return render_template('editar_produccion_intelectual.html', produccion=produccion)
    else:
        flash('Producción Intelectual no encontrada')
        return redirect(url_for('produccion_intelectual'))

# Ruta para eliminar una producción intelectual
@app.route('/eliminar_produccion/<int:id_produccion>', methods=['POST'])
@login_required
def eliminar_produccion(id_produccion):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM produccionintelectual 
        WHERE id_produccion = %s AND id_usuario = %s
    """, (id_produccion, current_user.id))
    result = cur.fetchone()
    if result and result[0]:
        id_imagen = result[0]
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar la producción intelectual
    cur.execute("DELETE FROM produccionintelectual WHERE id_produccion = %s AND id_usuario = %s", (id_produccion, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Producción Intelectual eliminada correctamente')
    return redirect(url_for('produccion_intelectual'))

# --- NUEVA RUTA PARA RECONOCIMIENTOS ---

# Ruta para listar y agregar reconocimientos
@app.route('/reconocimientos', methods=['GET', 'POST'])
@login_required
def reconocimientos():
    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        institucion = request.form['institucion']
        fecha = request.form['fecha']
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar el reconocimiento
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO reconocimientos (id_usuario, tipo, descripcion, institucion, fecha, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, tipo, descripcion, institucion, fecha, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Reconocimiento agregado correctamente')
        return redirect(url_for('reconocimientos'))

    # Obtener los reconocimientos del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT r.id_reconocimiento, r.tipo, r.descripcion, r.institucion, r.fecha, r.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM reconocimientos r
        LEFT JOIN imagenesadjuntas ia ON r.id_imagen = ia.id_imagen
        WHERE r.id_usuario = %s
    """, [current_user.id])
    reconocimientos = cur.fetchall()
    cur.close()

    return render_template('reconocimientos.html', reconocimientos=reconocimientos)

# Ruta para editar un reconocimiento
@app.route('/editar_reconocimiento/<int:id_reconocimiento>', methods=['GET', 'POST'])
@login_required
def editar_reconocimiento(id_reconocimiento):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        institucion = request.form['institucion']
        fecha = request.form['fecha']
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM reconocimientos 
            WHERE id_reconocimiento = %s AND id_usuario = %s
        """, (id_reconocimiento, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, descripcion, id_imagen_actual))
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

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos del reconocimiento
        cur.execute("""
            UPDATE reconocimientos 
            SET tipo = %s, descripcion = %s, institucion = %s, fecha = %s, puntaje = %s
            WHERE id_reconocimiento = %s AND id_usuario = %s
        """, (tipo, descripcion, institucion, fecha, puntaje, id_reconocimiento, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Reconocimiento actualizado correctamente')
        return redirect(url_for('reconocimientos'))

    # Obtener los datos actuales del reconocimiento
    cur.execute("""
        SELECT r.id_reconocimiento, r.tipo, r.descripcion, r.institucion, r.fecha, r.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM reconocimientos r
        LEFT JOIN imagenesadjuntas ia ON r.id_imagen = ia.id_imagen
        WHERE r.id_reconocimiento = %s AND r.id_usuario = %s
    """, (id_reconocimiento, current_user.id))
    reconocimiento = cur.fetchone()
    cur.close()

    if reconocimiento:
        return render_template('editar_reconocimiento.html', reconocimiento=reconocimiento)
    else:
        flash('Reconocimiento no encontrado')
        return redirect(url_for('reconocimientos'))

# Ruta para eliminar un reconocimiento
@app.route('/eliminar_reconocimiento/<int:id_reconocimiento>', methods=['POST'])
@login_required
def eliminar_reconocimiento(id_reconocimiento):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM reconocimientos 
        WHERE id_reconocimiento = %s AND id_usuario = %s
    """, (id_reconocimiento, current_user.id))
    result = cur.fetchone()
    if result and result[0]:
        id_imagen = result[0]
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar el reconocimiento
    cur.execute("DELETE FROM reconocimientos WHERE id_reconocimiento = %s AND id_usuario = %s", (id_reconocimiento, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Reconocimiento eliminado correctamente')
    return redirect(url_for('reconocimientos'))

# --- NUEVA RUTA PARA SOFTWARE ESPECIALIZADO ---

@app.route('/softwareespecializado', methods=['GET', 'POST'])
@login_required
def softwareespecializado():
    if request.method == 'POST':
        # Capturar datos del formulario
        nombre_curso = request.form['nombre_curso']
        modalidad = request.form['modalidad']
        horas = request.form['horas']
        institucion = request.form['institucion']
        fecha_publicacion = request.form['fecha']
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
            """, (current_user.id, categoria, f"Archivo para {nombre_curso}", unique_filename))
            db.connection.commit()
            id_imagen = cur.lastrowid
            cur.close()
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar el software especializado
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO softwareespecializado (id_usuario, nombre_curso, modalidad, horas, institucion, fecha, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, nombre_curso, modalidad, horas, institucion, fecha_publicacion, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Software Especializado agregado correctamente')
        return redirect(url_for('softwareespecializado'))

    # Obtener los softwares especializados del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT se.id_software, se.nombre_curso, se.modalidad, se.horas,
               se.institucion, se.fecha, se.puntaje,
               ia.ruta_imagen, ia.categoria
        FROM softwareespecializado se
        LEFT JOIN imagenesadjuntas ia ON se.id_imagen = ia.id_imagen
        WHERE se.id_usuario = %s
    """, [current_user.id])
    softwares = cur.fetchall()
    cur.close()

    return render_template('softwareespecializado.html', softwares=softwares)

# Ruta para editar un software especializado
@app.route('/editar_softwareespecializado/<int:id_software>', methods=['GET', 'POST'])
@login_required
def editar_softwareespecializado(id_software):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        nombre_curso = request.form['nombre_curso']
        modalidad = request.form['modalidad']
        horas = request.form['horas']
        institucion = request.form['institucion']
        fecha_publicacion = request.form['fecha']
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM softwareespecializado 
            WHERE id_software = %s AND id_usuario = %s
        """, (id_software, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result['id_imagen'] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, f"Archivo para {nombre_curso}", id_imagen_actual))
            else:
                # Insertar un nuevo archivo
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, f"Archivo para {nombre_curso}", unique_filename))
                db.connection.commit()
                id_imagen_nueva = cur.lastrowid

                # Actualizar el software especializado con el nuevo id_imagen
                cur.execute("""
                    UPDATE softwareespecializado 
                    SET id_imagen = %s 
                    WHERE id_software = %s AND id_usuario = %s
                """, (id_imagen_nueva, id_software, current_user.id))

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos del software especializado
        cur.execute("""
            UPDATE softwareespecializado 
            SET nombre_curso = %s, modalidad = %s, horas = %s, institucion = %s, fecha = %s, puntaje = %s
            WHERE id_software = %s AND id_usuario = %s
        """, (nombre_curso, modalidad, horas, institucion, fecha_publicacion, puntaje, id_software, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Software Especializado actualizado correctamente')
        return redirect(url_for('softwareespecializado'))

    # Obtener los datos actuales del software especializado
    cur.execute("""
        SELECT se.id_software, se.nombre_curso, se.modalidad, se.horas,
               se.institucion, se.fecha, se.puntaje,
               ia.ruta_imagen, ia.categoria
        FROM softwareespecializado se
        LEFT JOIN imagenesadjuntas ia ON se.id_imagen = ia.id_imagen
        WHERE se.id_software = %s AND se.id_usuario = %s
    """, (id_software, current_user.id))
    software = cur.fetchone()
    cur.close()

    if software:
        return render_template('editar_softwareespecializado.html', software=software)
    else:
        flash('Software Especializado no encontrado')
        return redirect(url_for('softwareespecializado'))

# Ruta para eliminar un software especializado
@app.route('/eliminar_softwareespecializado/<int:id_software>', methods=['POST'])
@login_required
def eliminar_softwareespecializado(id_software):
    cur = db.connection.cursor()
    # Obtener id_imagen para eliminar la imagen adjunta si existe
    cur.execute("""
        SELECT id_imagen FROM softwareespecializado 
        WHERE id_software = %s AND id_usuario = %s
    """, (id_software, current_user.id))
    result = cur.fetchone()
    if result and result['id_imagen']:
        id_imagen = result['id_imagen']
        # Eliminar la imagen de la tabla imagenesadjuntas
        cur.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s AND id_usuario = %s", (id_imagen, current_user.id))
    # Eliminar el software especializado
    cur.execute("DELETE FROM softwareespecializado WHERE id_software = %s AND id_usuario = %s", (id_software, current_user.id))
    db.connection.commit()
    cur.close()
    flash('Software Especializado eliminado correctamente')
    return redirect(url_for('softwareespecializado'))

# --- NUEVA RUTA PARA TUTORÍAS ---

# Ruta para listar y agregar tutorías
@app.route('/tutorias', methods=['GET', 'POST'])
@login_required
def tutorias():
    if request.method == 'POST':
        # Capturar datos del formulario
        descripcion = request.form['descripcion']
        anio = request.form['anio']
        puntaje = request.form['puntaje']

        # Manejo de archivos (imagen o PDF)
        file = request.files.get('archivo')
        id_imagen = None
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
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
        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Insertar la tutoría
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO tutorias (id_usuario, descripcion, anio, puntaje, id_imagen)
            VALUES (%s, %s, %s, %s, %s)
        """, (current_user.id, descripcion, anio, puntaje, id_imagen))
        db.connection.commit()
        cur.close()

        flash('Tutoria agregada correctamente')
        return redirect(url_for('tutorias'))

    # Obtener las tutorías del usuario actual
    cur = db.connection.cursor()
    cur.execute("""
        SELECT t.id_tutoria, t.descripcion, t.anio, t.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM tutorias t
        LEFT JOIN imagenesadjuntas ia ON t.id_imagen = ia.id_imagen
        WHERE t.id_usuario = %s
    """, [current_user.id])
    tutorias = cur.fetchall()
    cur.close()

    return render_template('tutorias.html', tutorias=tutorias)

# Ruta para editar una tutoría
@app.route('/editar_tutoria/<int:id_tutoria>', methods=['GET', 'POST'])
@login_required
def editar_tutoria(id_tutoria):
    cur = db.connection.cursor()

    if request.method == 'POST':
        # Capturar datos del formulario
        descripcion = request.form['descripcion']
        anio = request.form['anio']
        puntaje = request.form['puntaje']
        file = request.files.get('archivo')

        # Obtener el id_imagen actual
        cur.execute("""
            SELECT id_imagen FROM tutorias 
            WHERE id_tutoria = %s AND id_usuario = %s
        """, (id_tutoria, current_user.id))
        result = cur.fetchone()
        id_imagen_actual = result[0] if result else None

        # Manejar el archivo si se sube uno nuevo
        if file and allowed_file(file.filename):
            # Procesar y guardar el archivo
            filename = secure_filename(file.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Determinar el tipo de archivo
            file_extension = filename.rsplit('.', 1)[1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                categoria = 'imagen'
            elif file_extension == 'pdf':
                categoria = 'pdf'
            else:
                flash('Debe seleccionar un archivo válido (imagen o PDF).')
                return redirect(request.url)

            if id_imagen_actual:
                # Actualizar el archivo existente
                cur.execute("""
                    UPDATE imagenesadjuntas 
                    SET ruta_imagen = %s, categoria = %s, descripcion = %s, fecha_subida = NOW()
                    WHERE id_imagen = %s
                """, (unique_filename, categoria, descripcion, id_imagen_actual))
            else:
                # Insertar un nuevo archivo
                cur.execute("""
                    INSERT INTO imagenesadjuntas (id_usuario, categoria, descripcion, ruta_imagen) 
                    VALUES (%s, %s, %s, %s)
                """, (current_user.id, categoria, descripcion, unique_filename))
                db.connection.commit()
                id_imagen_nueva = cur.lastrowid

                # Actualizar la tutoría con el nuevo id_imagen
                cur.execute("""
                    UPDATE tutorias 
                    SET id_imagen = %s 
                    WHERE id_tutoria = %s AND id_usuario = %s
                """, (id_imagen_nueva, id_tutoria, current_user.id))

        elif file:
            flash('Debe seleccionar un archivo válido (imagen o PDF).')
            return redirect(request.url)

        # Actualizar los datos de la tutoría
        cur.execute("""
            UPDATE tutorias 
            SET descripcion = %s, anio = %s, puntaje = %s
            WHERE id_tutoria = %s AND id_usuario = %s
        """, (descripcion, anio, puntaje, id_tutoria, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Tutoria actualizada correctamente')
        return redirect(url_for('tutorias'))

    # Obtener los datos actuales de la tutoría
    cur.execute("""
        SELECT t.id_tutoria, t.descripcion, t.anio, t.puntaje, 
               ia.ruta_imagen, ia.categoria
        FROM tutorias t
        LEFT JOIN imagenesadjuntas ia ON t.id_imagen = ia.id_imagen
        WHERE t.id_tutoria = %s AND t.id_usuario = %s
    """, (id_tutoria, current_user.id))
    tutoria = cur.fetchone()
    cur.close()

    if tutoria:
        return render_template('editar_tutoria.html', tutoria=tutoria)
    else:
        flash('Tutoria no encontrada')
        return redirect(url_for('tutorias'))

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
    flash('Tutoria eliminada correctamente')
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
            SELECT usuarios.id_usuario, usuarios.usuario, usuarios.rol,
            datospersonales.nombres, datospersonales.apellido_paterno, datospersonales.apellido_materno,
            datospersonales.dni, datospersonales.correo_personal, datospersonales.movil, datospersonales.codigo
            FROM usuarios
            LEFT JOIN datospersonales ON usuarios.id_usuario = datospersonales.id_usuario
            LIMIT %s OFFSET %s
        """, (resultados_por_pagina, offset))
        usuarios = cur.fetchall()
        cur.close()

    except Exception as e:
        flash('Ocurrió un error al obtener los datos del personal: {}'.format(str(e)), 'error')
        return redirect(url_for('home'))

    return render_template('admin_ver_datos_personal.html', usuarios=usuarios, page=page, total_paginas=total_paginas)

# --- FIN DE NUEVAS RUTAS ---

# Manejo de errores y configuración final
if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.run()