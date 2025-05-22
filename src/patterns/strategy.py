import random
from abc import ABC, abstractmethod

class DesempateStrategy(ABC):
    @abstractmethod
    def resolver(self, opciones_empate):
        pass

class DesempateAlfabetico(DesempateStrategy):
    def resolver(self, opciones_empate):
        return sorted(opciones_empate)[0]

class DesempateAleatorio(DesempateStrategy):
    def resolver(self, opciones_empate):
        return random.choice(opciones_empate)

class DesempateProrroga(DesempateStrategy):
    def resolver(self, opciones_empate):
        print("⚠️ Prórroga activada (simulado). Retornando la primera opción.")
        return opciones_empate[0]
