from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, usuario, contrasena, nombre_completo="", rol=None, estado="activo", create_at=None, update_at=None):
        self.id = id
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre_completo = nombre_completo
        self.rol = rol
        self.estado = estado
        self.create_at = create_at
        self.update_at = update_at

    @classmethod
    def check_password(cls, hashed_password, contrasena):
        """Compara una contraseña cifrada con la contraseña ingresada."""
        return check_password_hash(hashed_password, contrasena)
