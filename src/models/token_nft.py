import uuid
from datetime import datetime

class TokenNFT:
    def __init__(self, encuesta_id, opcion, propietario):
        self.id = str(uuid.uuid4())
        self.encuesta_id = encuesta_id
        self.opcion = opcion
        self.fecha = datetime.utcnow().isoformat()
        self.propietario = propietario  # username
    
class TokenNFT:
    def __init__(self, token_id, owner, poll_id, option, issued_at):
        self.token_id = token_id
        self.owner = owner
        self.poll_id = poll_id
        self.option = option
        self.issued_at = issued_at

    def to_dict(self):
        return {
            "token_id": self.token_id,
            "owner": self.owner,
            "poll_id": self.poll_id,
            "option": self.option,
            "issued_at": self.issued_at.isoformat()
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            token_id=d["token_id"],
            owner=d["owner"],
            poll_id=d["poll_id"],
            option=d["option"],
            issued_at=datetime.fromisoformat(d["issued_at"])
        )
