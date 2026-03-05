from datetime import date
from typing import List
from persona import Persona
from valorable import Valorable

class Monitor(Persona, Valorable):
    def __init__(self, nombre: str, dni: str, direccion: str, localidad: str, provincia: str, codigo_postal: str,
                telefono: str, fecha_nacimiento: date, especialidad: List, sueldo: float, votos_positivos: int, votos_negativos: int) -> None:
        super().__init__(nombre, dni, direccion, localidad, provincia, codigo_postal, telefono, fecha_nacimiento)
        if not self.validar_especialidad(especialidad):
            raise ValueError(f"Especialidad inválida: {especialidad}")
        if not self.validar_sueldo(sueldo):
            raise ValueError(f"Sueldo inválido: {sueldo}")
        if not self.validar_votos(votos_positivos):
            raise ValueError(f"Votos positivos inválidos: {votos_positivos}")
        if not self.validar_votos(votos_negativos):
            raise ValueError(f"Votos negativos inválidos: {votos_negativos}")
        self._especialidad = especialidad
        self._sueldo = sueldo
        self._votos_positivos = votos_positivos
        self._votos_negativos = votos_negativos
    
    @staticmethod
    def validar_especialidad(value: List) -> bool:
        if len(value) > 0 and len(value) <= 3:
            return True
        return False

    @staticmethod
    def validar_sueldo(value: float) -> bool:
        """Valida que el sueldo sea mayor o igual al salario mínimo.
        Args:
            value (float): El sueldo a validar.
        Returns:
            bool: True si el sueldo es válido, False en caso contrario."""
        if value >= 1184:
            return True
        return False
    
    @staticmethod
    def validar_votos(value: int) -> bool:
        """Valida que el número de votos sea un entero no negativo.
        Args:
            value (int): El número de votos a validar.
        Returns:
            bool: True si el número de votos es válido, False en caso contrario."""
        if isinstance(value, int) and value >= 0:
            return True
        return False
    
    def __copy__(self) -> 'Monitor':
        """Crea una copia del monitor actual.
        
        Returns:
            Monitor: Una nueva instancia de Monitor con los mismos datos que el monitor actual.
        """
        return Monitor(self.nombre, self.dni, self.direccion, self.localidad, self.provincia, self.codigo_postal,
                    self.telefono, self.fecha_nacimiento, self._especialidad.copy(), self._sueldo, self._votos_positivos, self._votos_negativos)
    
    def __str__(self) -> str:
        """Devuelve una representación en cadena del monitor, incluyendo su información personal y detalles profesionales.
        
        Returns:
            str: Representación en cadena del monitor.
        """
        return super().__str__() + f", Especialidad: {', '.join(self._especialidad)}, Sueldo: {self._sueldo}, Votos positivos: {self._votos_positivos}, Votos negativos: {self._votos_negativos}"
    
    # GETTERS Y SETTERS

    @property
    def especialidad(self) -> List:
        """Devuelve la lista de especialidades del monitor."""
        return self._especialidad
    
    @especialidad.setter
    def especialidad(self, value: List) -> None:
        """Establece la lista de especialidades del monitor.
        Args:
            value (List): La nueva lista de especialidades del monitor.
        
        Raises:
            ValueError: Si la lista de especialidades proporcionada no es válida.
        """
        if not self.validar_especialidad(value):
            raise ValueError(f"Especialidad inválida: {value}")
        self._especialidad = value

    @property
    def sueldo(self) -> float:
        """Devuelve el sueldo del monitor."""
        return self._sueldo
    
    @sueldo.setter
    def sueldo(self, value: float) -> None:
        """Establece el sueldo del monitor.
        Args:
            value (float): El nuevo sueldo del monitor.
        
        Raises:
            ValueError: Si el sueldo proporcionado no es válido.
        """
        if not self.validar_sueldo(value):
            raise ValueError(f"Sueldo inválido: {value}")
        self._sueldo = value

    @property
    def votos_positivos(self) -> int:
        """Devuelve el número de votos positivos del monitor."""
        return self._votos_positivos
    
    @votos_positivos.setter
    def votos_positivos(self, value: int) -> None:
        """Establece el número de votos positivos del monitor.
        Args:
            value (int): El nuevo número de votos positivos del monitor.
        
        Raises:
            ValueError: Si el número de votos positivos proporcionado no es válido.
        """
        if not self.validar_votos(value):
            raise ValueError(f"Votos positivos inválidos: {value}")
        self._votos_positivos = value

    @property
    def votos_negativos(self) -> int:
        """Devuelve el número de votos negativos del monitor."""
        return self._votos_negativos
    
    @votos_negativos.setter
    def votos_negativos(self, value: int) -> None:
        """Establece el número de votos negativos del monitor.
        Args:
            value (int): El nuevo número de votos negativos del monitor.
        
        Raises:
            ValueError: Si el número de votos negativos proporcionado no es válido.
        """
        if not self.validar_votos(value):
            raise ValueError(f"Votos negativos inválidos: {value}")
        self._votos_negativos = value

    def me_gusta(self, like: bool) -> None:
        """Incrementa el número de votos positivos o negativos del monitor según el valor de 'like'.
        Args:
            like (bool): Si es True, incrementa los votos positivos; si es False, incrementa los votos negativos.
        """
        if like:
            self._votos_positivos += 1
        else:
            self._votos_negativos += 1

    def calcular_valoracion(self) -> int:
        """Calcula la valoración del monitor dividiendo el número de votos positivos entre el total de votos y multiplicando por 10.
        
        Returns:
            int: La valoración del monitor como porcentaje (0-10).
        """
        
        votos_totales = self._votos_positivos + self._votos_negativos
        
        if votos_totales == 0:
            return 0
        
        return round((self._votos_positivos / votos_totales) * 10)