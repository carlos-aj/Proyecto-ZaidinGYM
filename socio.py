from persona import Persona

from datetime import date

class Socio(Persona):
    def __init__(self, nombre: str, dni: str, direccion: str, localidad: str, provincia: str, codigo_postal: str, 
                telefono: str, fecha_nacimiento: date, fecha_registro: date, ultimo_acceso: date, esta_activo: bool,
                cuota: float) -> None:
        super().__init__(nombre, dni, direccion, localidad, provincia, codigo_postal, telefono, fecha_nacimiento)
        self.__fecha_registro = fecha_registro
        self.__ultimo_acceso = ultimo_acceso
        self.__esta_activo = esta_activo
        self.__cuota = cuota
        self._lista_actividades = []       


