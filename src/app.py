import sys
from src.services.user_service import UserService
from src.services.poll_service import PollService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService

from src.repositories.usuario_repo import UsuarioRepository
from src.repositories.encuesta_repo import EncuestaRepository
from src.repositories.nft_repo import NFTRepository

from src.controllers.cli_controller import CLIController
# from src.ui.gradio_app import launch_gradio  # <- activaremos después

def main():
    args = sys.argv[1:]

    # Repositorios
    usuario_repo = UsuarioRepository()
    encuesta_repo = EncuestaRepository()
    nft_repo = NFTRepository()

    # Servicios
    user_service = UserService(usuario_repo)
    nft_service = NFTService(nft_repo)
    poll_service = PollService(encuesta_repo, nft_service)
    chatbot_service = ChatbotService(poll_service)

    if "--ui" in args:
        print("🔌 Modo interfaz Gradio (no implementado aún).")
        # launch_gradio(user_service, poll_service, nft_service, chatbot_service)
    else:
        controller = CLIController(user_service, poll_service, nft_service)
        controller.start()

if __name__ == "__main__":
    main()
