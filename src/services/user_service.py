import uuid
from src.models.usuario import Usuario
from src.repositories.usuario_repo import UsuarioRepository

class UserService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo
        self.sesiones = {}  # username → token de sesión

    def register(self, username, password):
        if self.repo.obtener_usuario(username):
            raise ValueError("El usuario ya existe")
        user = Usuario(username, password)
        self.repo.guardar_usuario(user)
        return True

    def login(self, username, password):
        user = self.repo.obtener_usuario(username)
        if not user or not user.verificar_password(password):
            raise ValueError("Credenciales inválidas")
        token = str(uuid.uuid4())
        self.sesiones[username] = token
        return token

    def esta_logueado(self, username):
        return username in self.sesiones

    def logout(self, username):
        if username in self.sesiones:
            del self.sesiones[username]