import json
import os
from datetime import datetime
from uuid import UUID
from src.models.token_nft import TokenNFT

class NFTRepository:
    def __init__(self, archivo="data/tokens.json"):
        self.archivo = archivo
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump([], f)

    def guardar_token(self, token: TokenNFT):
        tokens = self._cargar()
        tokens.append(token.to_dict())
        self._guardar(tokens)

    def actualizar_token(self, token: TokenNFT):
        tokens = self._cargar()
        for i, t in enumerate(tokens):
            if t["token_id"] == str(token.token_id):
                tokens[i] = token.to_dict()
                break
        self._guardar(tokens)

    def obtener_tokens_de_usuario(self, username):
        tokens = self._cargar()
        return [TokenNFT.from_dict(t) for t in tokens if t["owner"] == username]

    def obtener_token(self, token_id):
        tokens = self._cargar()
        for t in tokens:
            if t["token_id"] == str(token_id):
                return TokenNFT.from_dict(t)
        return None

    def _cargar(self):
        with open(self.archivo, "r") as f:
            return json.load(f)

    def _guardar(self, data):
        with open(self.archivo, "w") as f:
            json.dump(data, f, indent=2)
