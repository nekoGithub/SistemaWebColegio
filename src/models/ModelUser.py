from .entities.User import User
from werkzeug.security import check_password_hash  # Importa check_password_hash aquí

class ModelUser:

    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, usuario, contrasena, nombre_completo FROM users 
                     WHERE usuario = '{}'""".format(user.usuario)  # Cambia 'nombre_completo' por 'usuario'
            cursor.execute(sql)
            row = cursor.fetchone()

            if row:  # Si el usuario existe
                # Verificamos la contraseña
                if check_password_hash(row[2], user.contrasena):  # Verifica si la contraseña es correcta
                    return User(row[0], row[1], row[2], row[3])  # Retorna el objeto User con la contraseña
                else:
                    return None  # Contraseña incorrecta
            else:
                return None  # Usuario no encontrado
        except Exception as ex:
            raise Exception(f"Error en el login: {ex}")

    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, usuario, nombre_completo FROM users WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return User(row[0], row[1], None, row[2])  # Sin contraseña en este caso
            else:
                return None
        except Exception as ex:
            raise Exception(f"Error al obtener usuario por ID: {ex}")


