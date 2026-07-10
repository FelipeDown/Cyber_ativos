from abc import ABC, abstractmethod

class PersistenciaInventario(ABC):
    @abstractmethod
    def salvar(self, dados: list):
        """Método abstrato para salvar dados em um arquivo ou banco de dados."""
        pass

    @abstractmethod
    def carregar(self) -> list:
        """Método abstrato para carregar dados de um arquivo ou banco de dados."""
        pass