from abc import ABC, abstractmethod
from datetime import date
import re

class Persona(ABC):
    def __init__(self, nombre: str, dni: str, direccion: str, localidad: str, provincia: str, codigo_postal: str, telefono: str, fecha_nacimiento: date) -> None:
        """Constructor de la clase Persona.
        Args:
            nombre (str): Nombre completo de la persona.
            dni (str): Documento Nacional de Identidad de la persona.
            direccion (str): Dirección de residencia de la persona.
            localidad (str): Localidad donde reside la persona.
            provincia (str): Provincia donde reside la persona.
            codigo_postal (str): Código postal de la dirección de residencia.
            telefono (str): Número de teléfono de contacto de la persona.
            fecha_nacimiento (date): Fecha de nacimiento de la persona.

        Raises:
            ValueError: Si alguno de los datos proporcionados no es válido.
        """
        if not self.validar_cadena(nombre):
            raise ValueError(f"Nombre inválido: {nombre}")
        if not self.validar_dni(dni):
            raise ValueError(f"DNI inválido: {dni}")
        if not self.validar_cadena(direccion):
            raise ValueError(f"Dirección inválida: {direccion}")
        if not self.validar_cadena(localidad):
            raise ValueError(f"Localidad inválida: {localidad}")
        if not self.validar_cadena(provincia):
            raise ValueError(f"Provincia inválida: {provincia}")
        if not self.validar_codigo_postal(codigo_postal):
            raise ValueError(f"Código postal inválido: {codigo_postal}")
        if not self.validar_telefono(telefono):
            raise ValueError(f"Teléfono inválido: {telefono}")
        if not self.validar_fecha_nacimiento(fecha_nacimiento):
            raise ValueError(f"Fecha de nacimiento inválida: {fecha_nacimiento}")

        self._nombre = nombre
        self._dni = dni
        self._direccion = direccion
        self._localidad = localidad
        self._provincia = provincia
        self._codigo_postal = codigo_postal
        self._telefono = telefono
        self._fecha_nacimiento = fecha_nacimiento

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
    def validar_dni(dni: str) -> bool:
        """Valida el formato del DNI.
        Args:
            dni (str): Documento Nacional de Identidad a validar.
        
        Returns:
            bool: True si el DNI es válido, False en caso contrario.
        """
        
        if not dni or len(dni) != 9:
            return False
        
        dni = dni.upper()

        if re.match(r"^[0-9]{8}[A-Z]$", dni):
            return Persona._validar_letra_dni(dni)
        
        return False

    @staticmethod
    def _validar_letra_dni(dni: str) -> bool:
        """Método para validar la letra de control del DNI.
        Args:
            dni (str): DNI a validar.

        Returns:
            bool: True si la letra de control es válida, False en caso contrario.
        """
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        numero = int(dni[:8])
        letra = dni[8]
        return letras[numero % 23] == letra
    
    @staticmethod
    def validar_codigo_postal(codigo_postal: str) -> bool:
        """Valida el formato del código postal.
        Args:
            codigo_postal (str): Código postal a validar.
        
        Returns:
            bool: True si el código postal es válido, False en caso contrario.
        """
        return bool(re.match(r"^\d{5}$", codigo_postal))
    
    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        """Valida el formato del número de teléfono.
        Args:
            telefono (str): Número de teléfono a validar.
        
        Returns:
            bool: True si el número de teléfono es válido, False en caso contrario.
        """
        return bool(re.match(r"^\d{9}$", telefono))

    @staticmethod
    def validar_fecha_nacimiento(fecha_nacimiento: date) -> bool:
        """Valida que la fecha de nacimiento no sea futura.
        Args:
            fecha_nacimiento (date): Fecha de nacimiento a validar.
        
        Returns:
            bool: True si la fecha de nacimiento es válida, False en caso contrario.
        """
        return fecha_nacimiento <= date.today()
    
    def __str__(self) -> str:
        """Devuelve una representación en cadena de la persona.
        
        Returns:
            str: Representación en cadena de la persona.
        """
        return f"Nombre: {self.nombre}, DNI: {self.dni}, Dirección: {self.direccion}, Localidad: {self.localidad}, Provincia: {self.provincia}, Código Postal: {self.codigo_postal}, Teléfono: {self.telefono}, Fecha de Nacimiento: {self.fecha_nacimiento}, Edad: {self.edad()}"
    
    # GETTERS Y SETTERS

    @property
    def nombre(self) -> str:
        """Devuelve el nombre de la persona."""
        return self._nombre
    
    @nombre.setter
    def nombre(self, value: str) -> None:
        """Establece el nombre de la persona.
        Args:
            value (str): El nuevo nombre de la persona.
            
        Raises:
            ValueError: Si el nombre proporcionado no es válido.
        """
        if not self.validar_cadena(value):
            raise ValueError(f"Nombre inválido: {value}")
        self._nombre = value

    @property
    def dni(self) -> str:
        """Devuelve el DNI de la persona."""
        return self._dni
    
    @dni.setter
    def dni(self, value: str) -> None:
        """Establece el DNI de la persona.
        Args:
            value (str): El nuevo DNI de la persona.
            
        Raises:
            ValueError: Si el DNI proporcionado no es válido.
        """
        if not self.validar_dni(value):
            raise ValueError(f"DNI inválido: {value}")
        self._dni = value

    @property
    def direccion(self) -> str:
        """Devuelve la dirección de la persona."""
        return self._direccion
    
    @direccion.setter
    def direccion(self, value: str) -> None:
        """Establece la dirección de la persona.
        Args:
            value (str): La nueva dirección de la persona.
            
        Raises:
            ValueError: Si la dirección proporcionada no es válida.
        """
        if not self.validar_cadena(value):
            raise ValueError(f"Dirección inválida: {value}")
        self._direccion = value

    @property
    def localidad(self) -> str:
        """Devuelve la localidad de la persona."""
        return self._localidad
    
    @localidad.setter
    def localidad(self, value: str) -> None:
        """Establece la localidad de la persona.
        Args:
            value (str): La nueva localidad de la persona.

        Raises:
            ValueError: Si la localidad proporcionada no es válida.
        """
        if not self.validar_cadena(value):
            raise ValueError(f"Localidad inválida: {value}")
        self._localidad = value

    @property
    def provincia(self) -> str:
        """Devuelve la provincia de la persona."""
        return self._provincia
    
    @provincia.setter
    def provincia(self, value: str) -> None:
        """Establece la provincia de la persona.
        Args:
            value (str): La nueva provincia de la persona.
            
        Raises:
            ValueError: Si la provincia proporcionada no es válida.
        """
        if not self.validar_cadena(value):
            raise ValueError(f"Provincia inválida: {value}")
        self._provincia = value

    @property
    def codigo_postal(self) -> str:
        """Devuelve el código postal de la persona."""
        return self._codigo_postal
    
    @codigo_postal.setter
    def codigo_postal(self, value: str) -> None:
        """Establece el código postal de la persona.
        Args:
            value (str): El nuevo código postal de la persona.
            
        Raises:
            ValueError: Si el código postal proporcionado no es válido.
        """
        if not self.validar_codigo_postal(value):
            raise ValueError(f"Código postal inválido: {value}")
        self._codigo_postal = value

    @property
    def telefono(self) -> str:
        """Devuelve el teléfono de la persona."""
        return self._telefono
    
    @telefono.setter
    def telefono(self, value: str) -> None:
        """Establece el teléfono de la persona.
        Args:
            value (str): El nuevo teléfono de la persona.
            
        Raises:
            ValueError: Si el teléfono proporcionado no es válido.
        """
        if not self.validar_telefono(value):
            raise ValueError(f"Teléfono inválido: {value}")
        self._telefono = value

    @property
    def fecha_nacimiento(self) -> date:
        """Devuelve la fecha de nacimiento de la persona."""
        return self._fecha_nacimiento
    
    @fecha_nacimiento.setter
    def fecha_nacimiento(self, value: date) -> None:
        """Establece la fecha de nacimiento de la persona.
        Args:
            value (date): La nueva fecha de nacimiento de la persona.
        
        Raises:
            ValueError: Si la fecha de nacimiento proporcionada no es válida.
        """
        if not self.validar_fecha_nacimiento(value):
            raise ValueError(f"Fecha de nacimiento inválida: {value}")
        self._fecha_nacimiento = value
    
    def edad(self) -> int:
        """Calcula la edad de la persona en años.
        
        Returns:
            int: Edad de la persona en años.
        """
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad
    
    def __eq__(self, value: object) -> bool:
        """Compara dos objetos Persona por su DNI.
        
        Returns:
            bool: True si los objetos tienen el mismo DNI, False en caso contrario.
        """
        if not isinstance(value, Persona):
            return False
        return self.dni == value.dni
    
    def __lt__(self, value: object) -> bool:
        """Compara dos objetos Persona por su edad.
        
        Returns:
            bool: True si la persona es menor que la otra, False en caso contrario.
        """
        if not isinstance(value, Persona):
            return False
        return self.edad() < value.edad()