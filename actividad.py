from typing import List
from enum import Enum
import re
from valorable import Valorable

class Especialidad(Enum):
    FITNESS = "FITNESS"
    PISCINA = "PISCINA"
    CICLISMO = "CICLISMO"
    HIIT = "HIIT"
    CORE = "CORE"
    BAILE = "BAILE"
    BODYCARE = "BODYCARE"
    CARDIO = "CARDIO"

class Actividad(Valorable):
    def __init__(self, nombre: str, duracion: int, calorias: int, categoria: Especialidad, es_premium: bool, votos: List) -> None:
        """Inicializa una nueva instancia de la clase Actividad.
        Args:
            nombre (str): El nombre de la actividad.
            duracion (int): La duración de la actividad en minutos.
            calorias (int): Las calorías quemadas durante la actividad.
            categoria (Especialidad): La categoría de la actividad.
            es_premium (bool): Indica si la actividad es premium o no.
            votos (List): Lista de votos de los usuarios para la actividad.
            
        Raises:
            ValueError: Si alguno de los parámetros proporcionados no es válido.
        """
        if not self.validar_cadena(nombre):
            raise ValueError(f"Nombre de actividad inválido: {nombre}")
        if not self.validar_duracion(duracion):
            raise ValueError(f"Duración de actividad inválida: {duracion}")
        if not self.validar_calorias(calorias):
            raise ValueError(f"Calorías de actividad inválidas: {calorias}")
        if not self.validar_categoria(categoria):
            raise ValueError(f"Categoría de actividad inválida: {categoria}")
        if not self.validar_es_premium(es_premium):
            raise ValueError(f"Valor de 'es_premium' inválido: {es_premium}")
        if not self.validar_votos(votos):
            raise ValueError(f"Lista de votos inválida: {votos}")
        
        self._nombre = nombre
        self._duracion = duracion
        self._calorias = calorias
        self._categoria = categoria
        self._es_premium = es_premium
        self._votos = votos

    @staticmethod
    def validar_cadena(cadena: str) -> bool:
        """Valida el formato de una cadena.
        Args:
            cadena (str): Cadena a validar.
        
        Returns:
            bool: True si la cadena es válida, False en caso contrario.
        """
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s.,/-]{1,50}$", cadena))
    
    @staticmethod
    def validar_duracion(duracion: int) -> bool:
        """Valida que la duración de la actividad sea un entero positivo y no exceda las 2 horas (120 minutos).
        Args:
            duracion (int): Duración de la actividad en minutos.
        
        Returns:
            bool: True si la duración es válida, False en caso contrario.
        """
        if duracion > 1 and duracion <= 120:
            return True
        return False
    
    @staticmethod
    def validar_calorias(calorias: int) -> bool:
        """Valida que las calorías quemadas sean un entero positivo.
        Args:
            calorias (int): Calorías quemadas durante la actividad.
        
        Returns:
            bool: True si las calorías son válidas, False en caso contrario.
        """
        if calorias > 0:
            return True
        return False
    
    @staticmethod
    def validar_categoria(categoria: Especialidad) -> bool:
        """Valida que la categoría de la actividad sea una instancia de Especialidad.
        Args:
            categoria (Especialidad): Categoría de la actividad.
        
        Returns:
            bool: True si la categoría es válida, False en caso contrario.
        """
        return isinstance(categoria, Especialidad)
    
    @staticmethod
    def validar_es_premium(es_premium: bool) -> bool:
        """Valida que el valor de 'es_premium' sea un booleano.
        Args:
            es_premium (bool): Indica si la actividad es premium o no.
        
        Returns:
            bool: True si el valor es un booleano, False en caso contrario.
        """
        if isinstance(es_premium, bool):
            return True
        return False
    
    @staticmethod
    def validar_votos(votos: List) -> bool:
        """Valida que la lista de votos sea una lista de enteros no negativos.
        Con valores del 0 al 10
        Args:
            votos (List): Lista de votos a validar.
            
        Returns:
            bool: True si la lista de votos es válida, False en caso contrario.
        """
        if isinstance(votos, list) and all(isinstance(voto, int) and 0 <= voto <= 10 for voto in votos):
            return True
        return False
    
    def __str__(self) -> str:
        """Devuelve una representación en cadena de la actividad, incluyendo su nombre, duración, calorías quemadas,
        categoría, si es premium y la lista de votos.
        
        Returns:
            str: Representación en cadena de la actividad.
        """
        return f"Actividad: {self._nombre}, Duración: {self._duracion} minutos, Calorías: {self._calorias}, Categoría: {self._categoria.value}, Es premium: {self._es_premium}, Votos: {self._votos}"
    
    # GETTERS Y SETTERS

    @property
    def nombre(self) -> str:
        """Devuelve el nombre de la actividad."""
        return self._nombre
    
    @nombre.setter
    def nombre(self, value: str) -> None:
        """Establece el nombre de la actividad.
        Args:
            value (str): El nuevo nombre de la actividad.
        
        Raises:
            ValueError: Si el nombre proporcionado no es válido.
        """
        if not self.validar_cadena(value):
            raise ValueError(f"Nombre de actividad inválido: {value}")
        self._nombre = value

    @property
    def duracion(self) -> int:
        """Devuelve la duración de la actividad en minutos."""
        return self._duracion
    
    @duracion.setter
    def duracion(self, value: int) -> None:
        """Establece la duración de la actividad en minutos.
        Args:
            value (int): La nueva duración de la actividad en minutos.
        
        Raises:
            ValueError: Si la duración proporcionada no es válida.
        """
        if not self.validar_duracion(value):
            raise ValueError(f"Duración de actividad inválida: {value}")
        self._duracion = value

    @property
    def calorias(self) -> int:
        """Devuelve las calorías quemadas durante la actividad."""
        return self._calorias
    
    @calorias.setter
    def calorias(self, value: int) -> None:
        """Establece las calorías quemadas durante la actividad.
        Args:
            value (int): Las nuevas calorías quemadas durante la actividad.
        
        Raises:
            ValueError: Si las calorías proporcionadas no son válidas.
        """
        if not self.validar_calorias(value):
            raise ValueError(f"Calorías de actividad inválidas: {value}")
        self._calorias = value

    @property
    def categoria(self) -> Especialidad:
        """Devuelve la categoría de la actividad."""
        return self._categoria
    
    @categoria.setter
    def categoria(self, value: Especialidad) -> None:
        """Establece la categoría de la actividad.
        Args:
            value (Especialidad): La nueva categoría de la actividad.
        
        Raises:
            ValueError: Si la categoría proporcionada no es válida.
        """
        if not self.validar_categoria(value):
            raise ValueError(f"Categoría de actividad inválida: {value}")
        self._categoria = value

    @property
    def es_premium(self) -> bool:
        """Devuelve si la actividad es premium o no."""
        return self._es_premium
    
    @es_premium.setter
    def es_premium(self, value: bool) -> None:
        """Establece si la actividad es premium o no.
        Args:
            value (bool): El nuevo valor de 'es_premium' para la actividad.
        
        Raises:
            ValueError: Si el valor proporcionado para 'es_premium' no es válido.
        """
        if not self.validar_es_premium(value):
            raise ValueError(f"Valor de 'es_premium' inválido: {value}")
        self._es_premium = value

    def __eq__(self, value) -> bool:
        """Compara dos actividades para determinar si son iguales, basándose en su nombre, duración, calorías quemadas,
        categoría, si son premium y la lista de votos.
        
        Args:
            value (Actividad): La actividad con la que se va a comparar la actividad actual.
        """
        if not isinstance(value, Actividad):
            return NotImplemented
        return (self._nombre == value._nombre and
                self._duracion == value._duracion and
                self._calorias == value._calorias and
                self._categoria == value._categoria and
                self._es_premium == value._es_premium and
                self._votos == value._votos)
    
    def __lt__(self, value) -> bool:
        """Compara dos actividades para determinar si la actividad actual es menor que la actividad proporcionada,
        basándose en el nombre de la actividad. De ser iguales, se comparará la duración de la actividad.
        
        Args:
            value (Actividad): La actividad con la que se va a comparar la actividad actual.
        
        Returns:
            bool: True si la actividad actual es menor que la actividad proporcionada, False en caso contrario.
        """
        if not isinstance(value, Actividad):
            return NotImplemented
        if self._nombre == value._nombre:
            return self._duracion < value._duracion
        return self._nombre < value._nombre

    def votar(self, voto: int) -> bool:
        """Agrega un voto a la lista de votos de la actividad.
        
        Args:
            voto (int): El voto a agregar a la lista de votos de la actividad.
        
        Raises:
            ValueError: Si el voto proporcionado no es válido.

        Returns:
            True si el voto es válido y se ha agregado a la lista de votos, False en caso contrario.
        """
        if not self.validar_votos([voto]):
            raise ValueError(f"Voto inválido: {voto}")
        self._votos.append(voto)
        return True
    
    def calcular_valoracion(self) -> int:
        """Calcula la valoración media de la actividad basada en los votos.
        
        Returns:
            int: La valoración promedio redondeada al entero más cercano.
                Retorna 0 si no hay votos.
        """
        if not self._votos:
            return 0
        return round(sum(self._votos) / len(self._votos))