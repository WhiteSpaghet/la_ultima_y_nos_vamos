import sys
from src.services.user_service import UserService
from src.services.poll_service import PollService
from src.services.nft_service import NFTService

class CLIController:
    def __init__(self, user_service: UserService, poll_service: PollService, nft_service: NFTService):
        self.user_service = user_service
        self.poll_service = poll_service
        self.nft_service = nft_service
        self.usuario_actual = None

    def start(self):
        print("👋 Bienvenido a la plataforma de votación interactiva")
        while True:
            cmd = input(">> ").strip()
            if cmd == "salir":
                print("👋 Adiós.")
                break
            try:
                self.parse_comando(cmd)
            except Exception as e:
                print(f"❌ Error: {e}")

    def parse_comando(self, cmd):
        partes = cmd.split()
        if not partes:
            return

        if partes[0] == "registrar":
            username = input("Username: ")
            password = input("Password: ")
            self.user_service.register(username, password)
            print("✅ Usuario registrado.")

        elif partes[0] == "login":
            username = input("Username: ")
            password = input("Password: ")
            if self.user_service.login(username, password):
                self.usuario_actual = username
                print(f"✅ Bienvenido, {username}.")
            else:
                print("❌ Login fallido.")

        elif partes[0] == "crear_encuesta":
            if not self.usuario_actual:
                raise Exception("Debes iniciar sesión.")
            pregunta = input("Pregunta: ")
            opciones = input("Opciones (separadas por coma): ").split(",")
            duracion = int(input("Duración en segundos: "))
            tipo = input("Tipo (simple/multiple): ")
            encuesta = self.poll_service.crear_encuesta(pregunta, opciones, duracion, tipo)
            print(f"✅ Encuesta creada con ID: {encuesta.id}")

        elif partes[0] == "votar":
            if not self.usuario_actual:
                raise Exception("Debes iniciar sesión.")
            poll_id = input("ID de la encuesta: ")
            opcion = input("Opción a votar: ")
            self.poll_service.votar(poll_id, self.usuario_actual, opcion)
            print("✅ Voto registrado.")

        elif partes[0] == "cerrar_encuesta":
            poll_id = input("ID de la encuesta: ")
            self.poll_service.cerrar_encuesta(poll_id)
            print("✅ Encuesta cerrada.")

        elif partes[0] == "resultados":
            poll_id = input("ID de la encuesta: ")
            resultados = self.poll_service.obtener_resultados_finales(poll_id)
            print("📊 Resultados:")
            for opcion, datos in resultados.items():
                print(f"- {opcion}: {datos['conteo']} votos ({datos['porcentaje']}%)")

        elif partes[0] == "mis_tokens":
            if not self.usuario_actual:
                raise Exception("Debes iniciar sesión.")
            tokens = self.nft_service.obtener_tokens_usuario(self.usuario_actual)
            print(f"🎟️ Tokens de {self.usuario_actual}:")
            for t in tokens:
                print(f"- ID: {t.token_id} | Encuesta: {t.poll_id} | Opción: {t.option} | Fecha: {t.issued_at}")

        elif partes[0] == "transferir_token":
            if not self.usuario_actual:
                raise Exception("Debes iniciar sesión.")
            token_id = input("ID del token: ")
            nuevo_owner = input("Nuevo propietario: ")
            self.nft_service.transferir_token(token_id, nuevo_owner, self.usuario_actual)
            print("✅ Token transferido.")

        else:
            print("❓ Comando desconocido.")
