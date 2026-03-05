from abc import ABC, abstractmethod

class Valorable(ABC):
    """Interface"""
    @abstractmethod
    def calcular_valoracion(self) -> int:
        pass