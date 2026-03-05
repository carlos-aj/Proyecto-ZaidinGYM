
from datetime import date
from actividad import Actividad
from socio import Socio

    
class SocioPremium(Socio):
    def __init__(self, nombre: str, dni: str, direccion: str, localidad: str, provincia: str, codigo_postal: str,
                telefono: str, fecha_nacimiento: date, fecha_registro: date, ultimo_acceso: date, esta_activo: bool) -> None:
        super().__init__(nombre, dni, direccion, localidad, provincia, codigo_postal,
                        telefono, fecha_nacimiento, fecha_registro, ultimo_acceso, esta_activo)
        
    def add_actvidad(self, a: Actividad) -> bool:
        """Agrega una actividad a la lista de actividades del socio. 
            Los socios premium pueden agregar cualquier actividad sin restricciones.
        Args:
            a (Actividad): La actividad a agregar.
        
        Returns:
            bool: True si la actividad se agregó correctamente.
        """
        self.lista_actividades.append(a)
        return True