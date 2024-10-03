# src/app.py
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import time

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