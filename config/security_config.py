import os
from cryptography.fernet import Fernet

# Variables de entorno
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("Faltan variables de entorno requeridas")

# Configuración de seguridad
class SecurityConfig:
    def __init__(self):
        self.API_ID = API_ID
        self.API_HASH = API_HASH
        self.BOT_TOKEN = BOT_TOKEN
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.max_login_attempts = 3
        self.lockout_duration = 1800
        self.password_min_length = 12
        self.require_2fa = True
