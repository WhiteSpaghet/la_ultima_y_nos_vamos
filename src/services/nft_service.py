import uuid
from datetime import datetime
from src.models.token_nft import TokenNFT
from src.repositories.nft_repo import NFTRepository

class NFTService:
    def __init__(self, repo: NFTRepository):
        self.repo = repo

    def mint_token(self, username, poll_id, opcion):
        token = TokenNFT(
            token_id=str(uuid.uuid4()),
            owner=username,
            poll_id=poll_id,
            option=opcion,
            issued_at=datetime.now()
        )
        self.repo.guardar_token(token)
        return token

    def transferir_token(self, token_id, nuevo_owner, usuario_actual):
        token = self.repo.obtener_token(token_id)
        if not token:
            raise ValueError("Token no encontrado")
        if token.owner != usuario_actual:
            raise ValueError("No eres el propietario de este token")
        token.owner = nuevo_owner
        self.repo.actualizar_token(token)

    def obtener_tokens_usuario(self, username):
        return self.repo.obtener_tokens_de_usuario(username)
