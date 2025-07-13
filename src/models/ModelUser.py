# src/models/ModelUser.py

from .entities.User import User
import bcrypt
import re
import logging # MEJORA: Usar el módulo de logging estándar de Python

# Configuración básica de logging
logging.basicConfig(filename='flask_app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

class ModelUser():

    # MEJORA 1: Aplicar el principio DRY (No te repitas)
    # Definimos la consulta base y el método de mapeo en un solo lugar.
    _BASE_QUERY = """
        SELECT u.id_usuario, u.usuario, u.contraseña, 
               CONCAT_WS(' ', dp.nombres, dp.apellido_paterno, dp.apellido_materno) AS fullname, u.rol
        FROM usuarios u
        LEFT JOIN datospersonales dp ON u.id_usuario = dp.id_usuario
        """

    @classmethod
    def _map_row_to_user(cls, row):
        """Mapea una fila de la base de datos a un objeto User."""
        if row:
            # Creamos el objeto User sin exponer la contraseña hash.
            # La contraseña solo se usa internamente para la verificación.
            return User(id=row[0], username=row[1], password=None, fullname=row[3], role=row[4])
        return None

    @classmethod
    def login(cls, db, user_entity):
        try:
            cursor = db.connection.cursor()
            # Reutilizamos la consulta base
            sql = cls._BASE_QUERY + " WHERE u.usuario = %s"
            cursor.execute(sql, (user_entity.username,))
            row = cursor.fetchone()

            if row:
                # Comparamos la contraseña usando el hash de la BD (row[2])
                if User.check_password(row[2], user_entity.password):
                    # Devolvemos un objeto User mapeado y limpio
                    return cls._map_row_to_user(row)
            return None # Si el usuario no existe o la contraseña es incorrecta
        except Exception as ex:
            logging.error(f"Error en ModelUser.login: {ex}")
            raise Exception("Error al intentar iniciar sesión.")

    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = cls._BASE_QUERY + " WHERE u.id_usuario = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            return cls._map_row_to_user(row)
        except Exception as ex:
            logging.error(f"Error en ModelUser.get_by_id: {ex}")
            raise Exception("Error al obtener el usuario por ID.")
            
    @classmethod
    def get_all_users(cls, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute(cls._BASE_QUERY)
            rows = cursor.fetchall()
            return [cls._map_row_to_user(row) for row in rows]
        except Exception as ex:
            logging.error(f"Error en ModelUser.get_all_users: {ex}")
            raise Exception("Error al obtener todos los usuarios.")

    # MEJORA 2: La creación del usuario debe recibir los datos por separado.
    @classmethod
    def create_user(cls, db, username, password, role, fullname, dni, codigo):
        """Crea un nuevo usuario y su entrada en datospersonales de forma atómica."""
        try:
            cursor = db.connection.cursor()
            
            # Hashear la contraseña
            hashed_password = cls.hash_password(password)
            
            # Insertar en la tabla 'usuarios'
            sql_user = "INSERT INTO usuarios (usuario, contraseña, rol) VALUES (%s, %s, %s)"
            cursor.execute(sql_user, (username, hashed_password, role))
            user_id = cursor.lastrowid # Obtener el ID del nuevo usuario

            # Insertar en la tabla 'datospersonales'
            # Asumimos que fullname es un diccionario o un objeto con los campos necesarios
            sql_dp = """
            INSERT INTO datospersonales (id_usuario, nombres, apellido_paterno, apellido_materno, dni, codigo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_dp, (
                user_id, 
                fullname.get('nombres', ''),
                fullname.get('apellido_paterno', ''),
                fullname.get('apellido_materno', ''),
                dni,
                codigo
            ))

            # MEJORA 3: Confirmar la transacción solo si todo fue exitoso
            db.connection.commit()
        except Exception as ex:
            # Si algo falla, deshacer todos los cambios
            db.connection.rollback()
            logging.error(f"Error en ModelUser.create_user: {ex}")
            raise Exception("Error al crear el usuario.")
    
    @classmethod
    def update_user(cls, db, user_id, username, role):
        """Actualiza los datos de un usuario."""
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE usuarios SET usuario = %s, rol = %s WHERE id_usuario = %s"
            cursor.execute(sql, (username, role, user_id))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            logging.error(f"Error en ModelUser.update_user: {ex}")
            raise Exception("Error al actualizar el usuario.")

    @classmethod
    def delete_user(cls, db, user_id):
        """Elimina un usuario. La BD se encargará de borrar en cascada."""
        try:
            cursor = db.connection.cursor()
            # La restricción ON DELETE CASCADE en la BD se encargará de datospersonales
            sql = "DELETE FROM usuarios WHERE id_usuario = %s"
            cursor.execute(sql, (user_id,))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            logging.error(f"Error en ModelUser.delete_user: {ex}")
            raise Exception("Error al eliminar el usuario.")
            
    @classmethod
    def update_password(cls, db, user_id, new_password):
        try:
            hashed_password = cls.hash_password(new_password)
            cursor = db.connection.cursor()
            sql = "UPDATE usuarios SET contraseña = %s WHERE id_usuario = %s"
            cursor.execute(sql, (hashed_password, user_id))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            logging.error(f"Error en ModelUser.update_password: {ex}")
            raise Exception("Error al actualizar la contraseña.")

    # --- Métodos de utilidad (Helpers) ---

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @classmethod
    def is_password_strong(cls, password):
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."
        if not re.search(r'[A-Z]', password):
            return False, "La contraseña debe tener al menos una letra mayúscula."
        if not re.search(r'[a-z]', password):
            return False, "La contraseña debe tener al menos una letra minúscula."
        if not re.search(r'\d', password):
            return False, "La contraseña debe tener al menos un número."
        return True, ""