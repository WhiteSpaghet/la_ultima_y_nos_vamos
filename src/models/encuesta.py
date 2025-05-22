from datetime import datetime
from enum import Enum

class EstadoEncuesta(Enum):
    ACTIVA = "activa"
    CERRADA = "cerrada"

class Encuesta:
    def __init__(self, id, pregunta, opciones, duracion_segundos):
        self.id = id
        self.pregunta = pregunta
        self.opciones = opciones  # Lista de strings
        self.votos = {op: 0 for op in opciones}
        self.estado = EstadoEncuesta.ACTIVA
        self.timestamp_inicio = datetime.utcnow()
        self.duracion_segundos = duracion_segundos

    def votar(self, opcion):
        if self.estado == EstadoEncuesta.CERRADA:
            raise Exception("La encuesta está cerrada.")
        if opcion not in self.votos:
            raise Exception("Opción no válida.")
        self.votos[opcion] += 1

    def cerrar(self):
        self.estado = EstadoEncuesta.CERRADA

    def esta_activa(self):
        if self.estado == EstadoEncuesta.CERRADA:
            return False
        delta = datetime.utcnow() - self.timestamp_inicio
        return delta.total_seconds() < self.duracion_segundos