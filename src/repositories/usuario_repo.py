import json
import os
from src.models.usuario import Usuario

class UsuarioRepository:
    def __init__(self, ruta_archivo="data/usuarios.json"):
        self.ruta_archivo = ruta_archivo
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w") as f:
                json.dump({}, f)

    def guardar_usuario(self, usuario: Usuario):
        usuarios = self._cargar_usuarios()
        usuarios[usuario.username] = {
            "password_hash": usuario.password_hash.decode(),
            "tokens": usuario.tokens
        }
        self._guardar_usuarios(usuarios)

    def obtener_usuario(self, username):
        usuarios = self._cargar_usuarios()
        if username not in usuarios:
            return None
        datos = usuarios[username]
        user = Usuario(username, "__dummy__")  # bypass del constructor
        user.password_hash = datos["password_hash"].encode()
        user.tokens = datos["tokens"]
        return user

    def _cargar_usuarios(self):
        with open(self.ruta_archivo, "r") as f:
            return json.load(f)

    def _guardar_usuarios(self, data):
        with open(self.ruta_archivo, "w") as f:
            json.dump(data, f, indent=2)