from .entities.User import User
import bcrypt
import re
from flask import flash

class ModelUser():

    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """
            SELECT usuarios.id_usuario, usuarios.usuario, usuarios.contraseña, CONCAT(datospersonales.nombres, ' ', datospersonales.apellido_paterno, ' ', datospersonales.apellido_materno) AS fullname, usuarios.rol
            FROM usuarios
            LEFT JOIN datospersonales ON usuarios.id_usuario = datospersonales.id_usuario
            WHERE usuarios.usuario = %s
            """
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()

            if row is not None:
                if len(row) == 5:
                    hashed_password = row[2]
                    if hashed_password:
                        if User.check_password(hashed_password, user.password):
                            user = User(row[0], row[1], True, row[3], row[4])
                            return user
                        else:
                            return None
                    else:
                        with open('errores.log', 'a') as f:
                            print("Error: La contraseña almacenada es inválida.", file=f)
                        return None
                else:
                    with open('errores.log', 'a') as f:
                        print("Error: La consulta no devolvió los 5 elementos esperados.", file=f)
                    return None
            else:
                return None
        except Exception as ex:
            with open('errores.log', 'a') as f:
                print(ex, file=f)
            raise Exception(ex)
        
    @classmethod
    def create_user(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """
            INSERT INTO usuarios (usuario, contraseña, rol)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (user.username, user.password, user.role))
            db.connection.commit()
            return True
        except Exception as ex:
            with open('errores.log', 'a') as f:
                print(ex, file=f)
            return False

    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """
            SELECT usuarios.id_usuario, usuarios.usuario, usuarios.contraseña, CONCAT(datospersonales.nombres, ' ', datospersonales.apellido_paterno, ' ', datospersonales.apellido_materno) AS fullname, usuarios.rol
            FROM usuarios
            LEFT JOIN datospersonales ON usuarios.id_usuario = datospersonales.id_usuario
            WHERE usuarios.id_usuario = %s
            """
            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row is not None:
                if len(row) == 5:
                    return User(row[0], row[1], row[2], row[3], row[4])
                else:
                    with open('errores.log', 'a') as f:
                        print("Error: La consulta no devolvió los 5 elementos esperados.", file=f)
                    return None
            else:
                return None
        except Exception as ex:
            with open('errores.log', 'a') as f:
                print(ex, file=f)
            raise Exception(ex)

    @classmethod
    def update_password(cls, db, user_id, new_password):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE usuarios SET contraseña = %s WHERE id_usuario = %s"
            cursor.execute(sql, (new_password, user_id))
            db.connection.commit()
            return True
        except Exception as ex:
            with open('errores.log', 'a') as f:
                print(ex, file=f)
            return False

    @classmethod
    def check_password(cls, hashed_password, password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @classmethod
    def is_password_strong(cls, password):
        # La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una minúscula, un número y un símbolo especial
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(pattern, password) is not None