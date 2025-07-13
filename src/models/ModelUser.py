# src/models/ModelUser.py

from .entities.User import User
import bcrypt
import re
import logging
from MySQLdb.cursors import DictCursor

# Configuración del logging para registrar errores y eventos importantes.
logging.basicConfig(filename='flask_app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

class ModelUser():
    """
    Clase modelo para gestionar todas las interacciones de la entidad Usuario con la base de datos.
    """

    # --- MÉTODOS INTERNOS PARA REUTILIZACIÓN DE CÓDIGO (PRINCIPIO DRY) ---

    @classmethod
    def _get_base_user_query(cls):
        """Devuelve la consulta SQL base para obtener usuarios con su nombre completo."""
        return """
            SELECT u.id_usuario, u.usuario, u.contraseña, u.rol,
                   CONCAT_WS(' ', dp.nombres, dp.apellido_paterno, dp.apellido_materno) AS fullname
            FROM usuarios u
            LEFT JOIN datospersonales dp ON u.id_usuario = dp.id_usuario
        """

    @classmethod
    def _map_row_to_user_entity(cls, row):
        """Mapea una fila de la base de datos a un objeto de la entidad User."""
        if row:
            # Creamos el objeto User sin exponer la contraseña hash.
            # La contraseña solo se usa internamente para la verificación.
            return User(id=row['id_usuario'], username=row['usuario'], password=None, fullname=row['fullname'], role=row['rol'])
        return None

    # --- MÉTODOS PÚBLICOS PARA LA GESTIÓN DE USUARIOS ---

    @classmethod
    def login(cls, db, user_entity):
        """Verifica las credenciales de un usuario y devuelve un objeto User si son válidas."""
        try:
            cursor = db.connection.cursor(DictCursor)
            sql = cls._get_base_user_query() + " WHERE u.usuario = %s"
            cursor.execute(sql, (user_entity.username,))
            row = cursor.fetchone()

            if row:
                # Comparamos la contraseña hasheada de la BD con la proporcionada por el usuario.
                if User.check_password(row['contraseña'], user_entity.password):
                    return cls._map_row_to_user_entity(row)
            return None # Si el usuario no existe o la contraseña es incorrecta
        except Exception as ex:
            logging.error(f"Error en ModelUser.login: {ex}")
            raise Exception("Error del sistema al intentar iniciar sesión.")

    @classmethod
    def get_by_id(cls, db, id):
        """Obtiene un usuario por su ID."""
        try:
            cursor = db.connection.cursor(DictCursor)
            sql = cls._get_base_user_query() + " WHERE u.id_usuario = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            return cls._map_row_to_user_entity(row)
        except Exception as ex:
            logging.error(f"Error en ModelUser.get_by_id: {ex}")
            raise Exception("Error del sistema al obtener el usuario.")

    @classmethod
    def get_all_users(cls, db):
        """Obtiene una lista de todos los usuarios del sistema."""
        try:
            cursor = db.connection.cursor(DictCursor)
            sql = cls._get_base_user_query() + " ORDER BY dp.apellido_paterno, dp.apellido_materno, dp.nombres ASC"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [cls._map_row_to_user_entity(row) for row in rows]
        except Exception as ex:
            logging.error(f"Error en ModelUser.get_all_users: {ex}")
            raise Exception("Error del sistema al obtener la lista de usuarios.")

    @classmethod
    def create_user(cls, db, username, password, role, fullname_data, dni, codigo):
        """Crea un nuevo usuario y su entrada en datospersonales de forma atómica."""
        try:
            cursor = db.connection.cursor()
            hashed_password = cls.hash_password(password)
            
            # Insertar en la tabla 'usuarios'
            sql_user = "INSERT INTO usuarios (usuario, contraseña, rol) VALUES (%s, %s, %s)"
            cursor.execute(sql_user, (username, hashed_password, role))
            user_id = cursor.lastrowid

            # Insertar en la tabla 'datospersonales'
            sql_dp = """
                INSERT INTO datospersonales (id_usuario, nombres, apellido_paterno, apellido_materno, dni, codigo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_dp, (
                user_id, fullname_data['nombres'], fullname_data['apellido_paterno'], 
                fullname_data['apellido_materno'], dni, codigo
            ))
            
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            logging.error(f"Error en ModelUser.create_user: {ex}")
            # El error más común es que el usuario ya exista (UNIQUE constraint)
            if 'Duplicate entry' in str(ex):
                raise Exception("El correo electrónico ya está en uso. Por favor, elige otro.")
            raise Exception("Error del sistema al crear el usuario.")
    
    @classmethod
    def get_user_with_details_by_id(cls, db, user_id):
        """Obtiene datos combinados para el formulario de edición."""
        try:
            cursor = db.connection.cursor(DictCursor)
            sql = """SELECT u.usuario, u.rol, dp.nombres, dp.apellido_paterno, dp.apellido_materno
                     FROM usuarios u
                     LEFT JOIN datospersonales dp ON u.id_usuario = dp.id_usuario
                     WHERE u.id_usuario = %s"""
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()
        except Exception as ex:
            raise Exception(f"Error al obtener detalles del usuario: {ex}")

    @classmethod
    def update_user_with_details(cls, db, user_id, username, nombres, apellido_paterno, apellido_materno):
        """Actualiza los datos de un usuario en ambas tablas de forma atómica."""
        try:
            cursor = db.connection.cursor()
            cursor.execute("UPDATE usuarios SET usuario = %s WHERE id_usuario = %s", (username, user_id))
            cursor.execute("""UPDATE datospersonales SET nombres=%s, apellido_paterno=%s, apellido_materno=%s
                              WHERE id_usuario = %s""", (nombres, apellido_paterno, apellido_materno, user_id))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"Error al actualizar los detalles del usuario: {ex}")

    @classmethod
    def update_password(cls, db, user_id, new_password):
        """Actualiza únicamente la contraseña de un usuario."""
        try:
            hashed_password = cls.hash_password(new_password)
            cursor = db.connection.cursor()
            sql = "UPDATE usuarios SET contraseña = %s WHERE id_usuario = %s"
            cursor.execute(sql, (hashed_password, user_id))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            logging.error(f"Error en ModelUser.update_password: {ex}")
            raise Exception("Error del sistema al actualizar la contraseña.")

    @classmethod
    def delete_user(cls, db, user_id):
        """Elimina un usuario. La restricción ON DELETE CASCADE de la BD se encarga del resto."""
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM usuarios WHERE id_usuario = %s"
            cursor.execute(sql, (user_id,))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            logging.error(f"Error en ModelUser.delete_user: {ex}")
            raise Exception("Error del sistema al eliminar el usuario.")

    @classmethod
    def get_paginated_docentes(cls, db, page, per_page):
        """Obtiene una lista paginada de docentes con sus detalles."""
        try:
            cursor = db.connection.cursor(DictCursor)
            cursor.execute("SELECT COUNT(*) as total FROM usuarios WHERE rol='Docente'")
            total_usuarios = cursor.fetchone()['total']
            total_paginas = (total_usuarios // per_page) + (1 if total_usuarios % per_page > 0 else 0)
            
            offset = (page - 1) * per_page
            
            sql = """
                SELECT u.id_usuario, u.usuario, dp.nombres, dp.apellido_paterno, dp.apellido_materno, dp.dni, dp.codigo
                FROM usuarios u LEFT JOIN datospersonales dp ON u.id_usuario = dp.id_usuario
                WHERE u.rol='Docente' ORDER BY dp.apellido_paterno ASC, dp.apellido_materno ASC LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (per_page, offset))
            usuarios = cursor.fetchall()
            
            return {'usuarios': usuarios, 'total_paginas': total_paginas}
        except Exception as ex:
            raise Exception(f"Error al obtener docentes paginados: {ex}")

    # --- MÉTODOS DE UTILIDAD (HELPERS) ---

    @classmethod
    def hash_password(cls, password):
        """Genera un hash de la contraseña usando bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @classmethod
    def is_password_strong(cls, password):
        """Verifica si una contraseña cumple con los criterios de seguridad."""
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."
        if not re.search(r'[A-Z]', password):
            return False, "La contraseña debe tener al menos una letra mayúscula."
        if not re.search(r'[a-z]', password):
            return False, "La contraseña debe tener al menos una letra minúscula."
        if not re.search(r'\d', password):
            return False, "La contraseña debe tener al menos un número."
        return True, ""