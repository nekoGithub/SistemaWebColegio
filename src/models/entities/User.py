from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, usuario, contrasena, nombre_completo="") -> None:
        self.id = id
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre_completo = nombre_completo

    @classmethod
    def check_password(self, hashed_password, contrasena):
        return check_password_hash(hashed_password, contrasena)