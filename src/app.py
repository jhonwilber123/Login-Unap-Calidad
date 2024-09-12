from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


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
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    cur = db.connection.cursor()
    cur.execute('SELECT id, username, fullname FROM personal')
    data = cur.fetchall()
    cur.close()
    return render_template('home.html', data=data)


@app.route('/add_personal', methods=['POST'])
@login_required
def add_personal():
    if request.method == 'POST':
        # Capturar los datos del formulario
        primer_nombre = request.form['primer_nombre']
        segundo_nombre = request.form['segundo_nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        direccion = request.form['direccion']
        celular = request.form['celular']
        correo_personal = request.form['correo_personal']
        correo_institucional = request.form['correo_institucional']
        numero_colegiatura = request.form['numero_colegiatura']
        codigo = request.form['codigo']
        dni = request.form['dni']
        fecha_nacimiento = request.form['fecha_nacimiento']
        lugar_nacimiento = request.form['lugar_nacimiento']
        departamento = request.form['departamento']
        provincia = request.form['provincia']
        distrito = request.form['distrito']
        es_docente = 'es_docente' in request.form
        es_administrativo = 'es_administrativo' in request.form
        condicion = request.form['condicion']
        categoria = request.form['categoria']
        dedicacion = request.form['dedicacion']
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']

        # Insertar los datos en la base de datos
        cur = db.connection.cursor()
        cur.execute("""
            INSERT INTO personal (primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, direccion, 
            celular, correo_personal, correo_institucional, numero_colegiatura, codigo, dni, fecha_nacimiento, 
            lugar_nacimiento, departamento, provincia, distrito, es_docente, es_administrativo, condicion, 
            categoria, dedicacion, username, password, fullname)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, direccion, celular, correo_personal, 
              correo_institucional, numero_colegiatura, codigo, dni, fecha_nacimiento, lugar_nacimiento, 
              departamento, provincia, distrito, es_docente, es_administrativo, condicion, categoria, dedicacion, 
              username, password, fullname))
        db.connection.commit()
        cur.close()

        flash('Personal agregado exitosamente')
        return redirect(url_for('home'))


@app.route('/edit_personal', methods=['GET', 'POST'])
@login_required
def edit_personal():
    if request.method == 'POST':
        # Capturar los datos del formulario editado
        primer_nombre = request.form['primer_nombre']
        segundo_nombre = request.form['segundo_nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        direccion = request.form['direccion']
        celular = request.form['celular']
        correo_personal = request.form['correo_personal']
        correo_institucional = request.form['correo_institucional']
        numero_colegiatura = request.form['numero_colegiatura']
        codigo = request.form['codigo']
        dni = request.form['dni']
        fecha_nacimiento = request.form['fecha_nacimiento']
        lugar_nacimiento = request.form['lugar_nacimiento']
        departamento = request.form['departamento']
        provincia = request.form['provincia']
        distrito = request.form['distrito']
        es_docente = 'es_docente' in request.form
        es_administrativo = 'es_administrativo' in request.form
        condicion = request.form['condicion']
        categoria = request.form['categoria']
        dedicacion = request.form['dedicacion']
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']

        # Actualizar los datos del usuario logueado en la base de datos
        cur = db.connection.cursor()
        cur.execute("""
            UPDATE personal
            SET primer_nombre = %s, segundo_nombre = %s, apellido_paterno = %s, apellido_materno = %s, 
            direccion = %s, celular = %s, correo_personal = %s, correo_institucional = %s, 
            numero_colegiatura = %s, codigo = %s, dni = %s, fecha_nacimiento = %s, lugar_nacimiento = %s, 
            departamento = %s, provincia = %s, distrito = %s, es_docente = %s, es_administrativo = %s, 
            condicion = %s, categoria = %s, dedicacion = %s, username = %s, password = %s, fullname = %s
            WHERE id = %s
        """, (primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, direccion, celular, 
              correo_personal, correo_institucional, numero_colegiatura, codigo, dni, fecha_nacimiento, 
              lugar_nacimiento, departamento, provincia, distrito, es_docente, es_administrativo, condicion, 
              categoria, dedicacion, username, password, fullname, current_user.id))
        db.connection.commit()
        cur.close()

        flash('Datos actualizados exitosamente')
        return redirect(url_for('home'))

    # Cargar los datos actuales del usuario logueado
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM personal WHERE id = %s', [current_user.id])
    data = cur.fetchone()
    cur.close()
    
    # Pasar los datos actuales al formulario para editar
    return render_template('edit_personal.html', data=data)


@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
