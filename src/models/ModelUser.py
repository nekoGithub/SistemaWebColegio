from .entities.User import User
from werkzeug.security import check_password_hash, generate_password_hash


class ModelUser:

    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, usuario, contrasena, nombre_completo, rol, estado FROM users 
                     WHERE usuario = '{}'""".format(user.usuario)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row:  # Si el usuario existe
                # Verificamos la contraseña
                if check_password_hash(row[2], user.contrasena):  # Verifica si la contraseña es correcta
                    return User(row[0], row[1], row[2], row[3], row[4], row[5])  # Retorna el objeto User
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
            sql = "SELECT id, usuario, contrasena, nombre_completo, rol, estado FROM users WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return User(row[0], row[1], row[2], row[3], row[4], row[5])  # Retorna el objeto User
            else:
                return None
        except Exception as ex:
            raise Exception(f"Error al obtener usuario por ID: {ex}")

    @staticmethod
    def get_all_users(db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, usuario, nombre_completo, rol, estado, created_at,updated_at FROM users WHERE estado='activo'"
            cursor.execute(sql)
            users = cursor.fetchall()
            return users
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def create_user(cls, db, user):
        try:
            cursor = db.connection.cursor()
            contrasena_encriptada = generate_password_hash(user.contrasena)
            # Si no se proporciona estado, se establece por defecto como 'activo'
            estado = user.estado if user.estado else 'activo'
            sql = """
                INSERT INTO users (usuario, contrasena, nombre_completo, rol, estado)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user.usuario, contrasena_encriptada, user.nombre_completo, user.rol, estado))
            db.connection.commit()
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False

    @staticmethod
    def update_user(db, user):
        try:
            cursor = db.connection.cursor()
            query = """
                UPDATE users
                SET usuario = %s, contrasena = %s, nombre_completo = %s, rol = %s
                WHERE id = %s
            """
            cursor.execute(query, (user.usuario, user.contrasena, user.nombre_completo, user.rol, user.id))
            db.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False

    @staticmethod
    def delete_user(db, user_id):
        cursor = db.connection.cursor()
        try:
            # Actualizamos el estado a 'inactivo' en lugar de eliminar el usuario
            cursor.execute("UPDATE users SET estado = 'inactivo' WHERE id = %s", (user_id,))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            raise ex
        finally:
            cursor.close()

