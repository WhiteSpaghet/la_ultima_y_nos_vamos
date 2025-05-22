import bcrypt

class Usuario:
    def __init__(self, username, password_plaintext):
        self.username = username
        self.password_hash = bcrypt.hashpw(password_plaintext.encode(), bcrypt.gensalt())
        self.tokens = []  # IDs de tokens NFT

    def verificar_password(self, password_plaintext):
        return bcrypt.checkpw(password_plaintext.encode(), self.password_hash)

    def agregar_token(self, token_id):
        self.tokens.append(token_id)