import json
import os
import uuid
from src.models.encuesta import Encuesta, EstadoEncuesta
from datetime import datetime

class EncuestaRepository:
    def __init__(self, archivo="data/encuestas.json"):
        self.archivo = archivo
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump({}, f)

    def guardar_encuesta(self, encuesta: Encuesta):
        data = self._cargar()
        data[encuesta.id] = {
            "pregunta": encuesta.pregunta,
            "opciones": encuesta.opciones,
            "votos": encuesta.votos,
            "estado": encuesta.estado.value,
            "timestamp_inicio": encuesta.timestamp_inicio.isoformat(),
            "duracion_segundos": encuesta.duracion_segundos
        }
        self._guardar(data)

    def obtener_encuesta(self, id):
        data = self._cargar()
        if id not in data:
            return None
        e = data[id]
        enc = Encuesta(
            id=id,
            pregunta=e["pregunta"],
            opciones=e["opciones"],
            duracion_segundos=e["duracion_segundos"]
        )
        enc.votos = e["votos"]
        enc.estado = EstadoEncuesta(e["estado"])
        enc.timestamp_inicio = datetime.fromisoformat(e["timestamp_inicio"])
        return enc

    def obtener_todas(self):
        data = self._cargar()
        return [self.obtener_encuesta(k) for k in data]

    def _cargar(self):
        with open(self.archivo, "r") as f:
            return json.load(f)

    def _guardar(self, data):
        with open(self.archivo, "w") as f:
            json.dump(data, f, indent=2)
