# src/models/entities/User.py

from flask_login import UserMixin
import bcrypt

class User(UserMixin):
    """
    Clase de Entidad que representa a un Usuario en el sistema.

    Esta clase no interactúa con la base de datos. Su única responsabilidad
    es contener los datos de un usuario de forma estructurada y proporcionar
    los métodos que Flask-Login necesita (heredados de UserMixin).
    """

    def __init__(self, id, username, role, fullname="", password=None):
        """
        Constructor de la entidad Usuario.
        
        Args:
            id (int): El ID único del usuario.
            username (str): El nombre de usuario (usualmente el correo).
            role (str): El rol del usuario ('Administrador', 'Docente', etc.).
            fullname (str, optional): El nombre completo del usuario.
            password (str, optional): La contraseña en texto plano (solo usada para la verificación de login).
                                      No se almacena en el objeto después de la inicialización.
        """
        self.id = id
        self.username = username
        self.role = role
        self.fullname = fullname
        
        # El atributo de contraseña en texto plano solo se usa temporalmente
        # para el proceso de login. No se almacena como un atributo de instancia.
        self._password_to_check = password

    @property
    def password(self):
        """
        Hacemos que el atributo de contraseña no sea directamente accesible.
        Si alguien intenta acceder a `user.password`, recibirá un error.
        Esto es una medida de seguridad para evitar exponer la contraseña accidentalmente.
        """
        raise AttributeError('La contraseña no es un atributo legible.')

    @classmethod
    def check_password(cls, hashed_password_from_db, password_to_check):
        """
        Método de clase para verificar si una contraseña en texto plano coincide
        con un hash de la base de datos.
        
        Args:
            hashed_password_from_db (str): El hash almacenado en la base de datos.
            password_to_check (str): La contraseña en texto plano enviada por el usuario.
        
        Returns:
            bool: True si las contraseñas coinciden, False en caso contrario.
        """
        try:
            # bcrypt necesita que los hashes y contraseñas estén en bytes.
            hashed_bytes = hashed_password_from_db.encode('utf-8')
            password_bytes = password_to_check.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except (ValueError, TypeError):
            # En caso de que el hash sea inválido o haya algún error,
            # devolvemos False por seguridad.
            return False

    # Los métodos que necesita Flask-Login como is_authenticated, get_id(), etc.,
    # son proporcionados automáticamente por la herencia de `UserMixin`.
    # No necesitamos definirlos explícitamente.