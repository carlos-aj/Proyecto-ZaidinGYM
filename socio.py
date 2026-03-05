from actividad import Actividad
from persona import Persona
from datetime import date

class Socio(Persona):
    def __init__(self, nombre: str, dni: str, direccion: str, localidad: str, provincia: str, codigo_postal: str, 
                telefono: str, fecha_nacimiento: date, fecha_registro: date, ultimo_acceso: date, esta_activo: bool) -> None:
        """Constructor de la clase Socio.
        Args:
            nombre (str): El nombre del socio.
            dni (str): El DNI del socio.
            direccion (str): La dirección del socio.
            localidad (str): La localidad del socio.
            provincia (str): La provincia del socio.
            codigo_postal (str): El código postal del socio.
            telefono (str): El teléfono del socio.
            fecha_nacimiento (date): La fecha de nacimiento del socio.
            fecha_registro (date): La fecha de registro del socio.
            ultimo_acceso (date): La fecha del último acceso del socio.
            esta_activo (bool): Indica si el socio está activo o no.
        
        Raises:
            ValueError: Si alguno de los datos proporcionados no es válido.
        """
        super().__init__(nombre, dni, direccion, localidad, provincia, codigo_postal, telefono, fecha_nacimiento)
        if not self.validar_fecha_registro(fecha_registro):
            raise ValueError(f"Fecha de registro inválida: {fecha_registro}")
        if not self.validar_ultimo_acceso(ultimo_acceso):
            raise ValueError(f"Último acceso inválido: {ultimo_acceso}")
        if not self.validar_esta_activo(esta_activo):
            raise ValueError(f"Valor de 'esta_activo' inválido: {esta_activo}")
        
        self._fecha_registro = fecha_registro
        self._ultimo_acceso = ultimo_acceso
        self._esta_activo = esta_activo
        self.__lista_actividades = []       
        self._cuota = self.calcular_cuota()       
    
    @staticmethod
    def validar_fecha_registro(value: date) -> bool:
        """Valida que la fecha de registro sea una fecha válida y no esté en el futuro.
        Args:
            value (date): La fecha de registro a validar.
            
        Returns:
            bool: True si la fecha de registro es válida, False en caso contrario.
        """
        return isinstance(value, date) and value <= date.today()
    
    @staticmethod
    def validar_ultimo_acceso(value: date) -> bool:
        """Valida que la fecha del último acceso sea una fecha válida y no esté en el futuro.
        Args:
            value (date): La fecha del último acceso a validar.
        
        Returns:
            bool: True si la fecha del último acceso es válida, False en caso contrario.
        """
        return isinstance(value, date) and value <= date.today()
    
    @staticmethod
    def validar_esta_activo(value: bool) -> bool:
        """Valida que el valor de 'esta_activo' sea un booleano.
        Args:
            value (bool): El valor a validar.
        
        Returns:
            bool: True si el valor es un booleano, False en caso contrario.
        """
        return isinstance(value, bool)
    
    def __copy__(self) -> 'Socio':
        """Crea una copia del socio actual.
        
        Returns:
            Socio: Una nueva instancia de Socio con los mismos datos que el socio actual.
        """
        return Socio(self.nombre, self.dni, self.direccion, self.localidad, self.provincia, self.codigo_postal,
                    self.telefono, self.fecha_nacimiento, self._fecha_registro, self._ultimo_acceso, self._esta_activo)

    def __str__(self) -> str:
        """Devuelve una representación en cadena del socio, incluyendo su información personal y detalles de registro.
        
        Returns:
            str: Representación en cadena del socio.
        """
        return super().__str__() + f", Fecha de registro: {self._fecha_registro}, Último acceso: {self._ultimo_acceso}, Está activo: {self._esta_activo}"
    
    # GETTERS Y SETTERS

    @property
    def fecha_registro(self) -> date:
        """Devuelve la fecha de registro del socio."""
        return self._fecha_registro
    
    @fecha_registro.setter
    def fecha_registro(self, value: date) -> None:
        """Establece la fecha de registro del socio.
        Args:
            value (date): La nueva fecha de registro del socio.
        
        Raises:
            ValueError: Si la fecha de registro proporcionada no es válida.
        """
        if not self.validar_fecha_registro(value):
            raise ValueError(f"Fecha de registro inválida: {value}")
        self._fecha_registro = value

    @property
    def ultimo_acceso(self) -> date:
        """Devuelve la fecha del último acceso del socio."""
        return self._ultimo_acceso
    
    @ultimo_acceso.setter
    def ultimo_acceso(self, value: date) -> None:
        """Establece la fecha del último acceso del socio.
        Args:
            value (date): La nueva fecha del último acceso del socio.
        
        Raises:
            ValueError: Si la fecha del último acceso proporcionada no es válida.
        """
        if not self.validar_ultimo_acceso(value):
            raise ValueError(f"Último acceso inválido: {value}")
        self._ultimo_acceso = value

    @property
    def esta_activo(self) -> bool:
        """Devuelve si el socio está activo o no."""
        return self._esta_activo
    
    @esta_activo.setter
    def esta_activo(self, value: bool) -> None:
        """Establece si el socio está activo o no.
        Args:
            value (bool): El nuevo valor de 'esta_activo' para el socio.
        
        Raises:
            ValueError: Si el valor proporcionado para 'esta_activo' no es válido.
        """
        if not self.validar_esta_activo(value):
            raise ValueError(f"Valor de 'esta_activo' inválido: {value}")
        self._esta_activo = value

    @property
    def cuota(self) -> float:
        """Devuelve la cuota del socio."""
        return self._cuota

    @property
    def lista_actividades(self) -> list:
        """Devuelve la lista de actividades del socio."""
        return self.__lista_actividades
    
    @lista_actividades.setter
    def lista_actividades(self, value: list) -> None:
        """Establece la lista de actividades del socio.
        Args:
            value: La nueva lista de actividades del socio.
        """
        self.__lista_actividades = value

    def get_duracion_actividades(self) -> int:
        """Calcula la duración total de las actividades del socio.
        
        Returns:
            int: La duración total de las actividades del socio en minutos.
        """
        return sum(actividad.duracion for actividad in self.__lista_actividades)
    
    def add_actvidad(self, a: Actividad) -> bool:
        """Agrega una actividad a la lista de actividades del socio."""
        if a.es_premium:
            raise ValueError(f"No se pueden agregar actividades premium a un socio no premium: {a}")
        self.__lista_actividades.append(a)
        return True

    def del_actividad(self, a: Actividad) -> bool:
        """Elimina una actividad de la lista de actividades del socio.
        Args:
            a (Actividad): La actividad a eliminar.
            
        Returns:
            bool: True si la actividad se eliminó correctamente, False si la actividad no se encontró en la lista de actividades del socio.
        """
        if a in self.__lista_actividades:
            self.__lista_actividades.remove(a)
            return True
        return False

    def calcular_cuota(self) -> float:
        """Calcula la cuota en base a las actividades del socio (6.5€/hora)
        
        Returns:
            float: La cuota del socio.
        """
        duracion_total = self.get_duracion_actividades()
        return (duracion_total / 60) * 6.5