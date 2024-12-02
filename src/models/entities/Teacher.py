from datetime import datetime

class Teacher:
    def __init__(self, id, nombres, apellidos, sexo, ci, num_celular=None, fecha_ingreso=None, estado="activo", id_user=None, create_at=None, update_at=None):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.sexo = sexo
        self.ci = ci
        self.num_celular = num_celular
        self.fecha_ingreso = fecha_ingreso
        self.estado = estado
        self.id_user = id_user
        self.create_at = create_at or datetime.now()  # Si no se proporciona, se establece la fecha y hora actual
        self.update_at = update_at or datetime.now()  # Similar para el update_at
