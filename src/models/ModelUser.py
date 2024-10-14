# src/models/entities/ModelUser.py

from .entities.User import User
import bcrypt

class ModelUser():

    @classmethod
    def login(self, db, user):
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
                        print("Error: La contraseña almacenada es inválida.")
                        return None
                else:
                    print("Error: La consulta no devolvió los 5 elementos esperados.")
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
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
                    print("Error: La consulta no devolvió los 5 elementos esperados.")
                    return None
            else:
                return None
        except Exception as ex:
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
            print(ex)
            return False
        
    @classmethod
    def check_password(cls, hashed_password, password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

