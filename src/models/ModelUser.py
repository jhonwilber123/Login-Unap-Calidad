# src/models/entities/ModelUser.py

from .entities.User import User

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
            SELECT usuarios.id_usuario, usuarios.usuario, CONCAT(datospersonales.nombres, ' ', datospersonales.apellido_paterno, ' ', datospersonales.apellido_materno) AS fullname, usuarios.rol
            FROM usuarios
            LEFT JOIN datospersonales ON usuarios.id_usuario = datospersonales.id_usuario
            WHERE usuarios.id_usuario = %s
            """
            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row is not None:
                if len(row) == 4:
                    return User(row[0], row[1], None, row[2], row[3])
                else:
                    print("Error: La consulta no devolvió los 4 elementos esperados.")
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
