import uuid
from src.models.encuesta import Encuesta
from src.repositories.encuesta_repo import EncuestaRepository
from src.services.nft_service import NFTService

class PollService:
    def __init__(self, repo: EncuestaRepository, nft_service: NFTService):
        self.repo = repo
        self.votaciones = {}  # encuesta_id → set(usernames)
        self.nft_service = nft_service

    def crear_encuesta(self, pregunta, opciones, duracion_segundos):
        poll_id = str(uuid.uuid4())
        encuesta = Encuesta(poll_id, pregunta, opciones, duracion_segundos)
        self.repo.guardar_encuesta(encuesta)
        self.votaciones[poll_id] = set()
        return poll_id

    def votar(self, poll_id, username, opcion):
        encuesta = self.repo.obtener_encuesta(poll_id)
        if not encuesta:
            raise ValueError("Encuesta no encontrada")
        if not encuesta.esta_activa():
            encuesta.cerrar()
            self.repo.guardar_encuesta(encuesta)
            raise ValueError("Encuesta cerrada")
        if username in self.votaciones.get(poll_id, set()):
            raise ValueError("Usuario ya ha votado")
        encuesta.votar(opcion)
        self.votaciones[poll_id].add(username)
        self.repo.guardar_encuesta(encuesta)
        self.nft_service.mint_token(username, poll_id, opcion)

    def cerrar_encuesta(self, poll_id):
        encuesta = self.repo.obtener_encuesta(poll_id)
        if encuesta and encuesta.estado.value == "activa":
            encuesta.cerrar()
            self.repo.guardar_encuesta(encuesta)

    def get_resultados_parciales(self, poll_id):
        encuesta = self.repo.obtener_encuesta(poll_id)
        if not encuesta:
            return None
        total = sum(encuesta.votos.values())
        return {
            opcion: {
                "votos": count,
                "porcentaje": (count / total * 100) if total else 0
            }
            for opcion, count in encuesta.votos.items()
        }
