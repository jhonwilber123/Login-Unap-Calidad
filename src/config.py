from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración
class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'gestion_personal'


config = {
    'development': DevelopmentConfig
}

# Aplicar configuración
app.config.from_object(config['development'])

# Inicializar MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    # Aquí puedes hacer una consulta a la base de datos
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT * FROM personals ''')
    data = cur.fetchall()
    cur.close()
    return str(data)

if __name__ == '__main__':
    app.run(debug=True)
