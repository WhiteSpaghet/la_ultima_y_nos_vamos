import uuid
from datetime import datetime

class TokenNFT:
    def __init__(self, encuesta_id, opcion, propietario):
        self.id = str(uuid.uuid4())
        self.encuesta_id = encuesta_id
        self.opcion = opcion
        self.fecha = datetime.utcnow().isoformat()
        self.propietario = propietario  # username