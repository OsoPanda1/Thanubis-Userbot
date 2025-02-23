import aiosqlite
import json
from cryptography.fernet import Fernet
from typing import Dict
from config.security_config import SecurityConfig

# Clase de base de datos segura
class SecureDatabase:
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.db_path = 'thanubis_secure.db'
        asyncio.run(self._initialize_db())

    async def _initialize_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
            PRAGMA foreign_keys = ON;
            PRAGMA journal_mode = WAL;
            PRAGMA synchronous = NORMAL;
            """)
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash BLOB NOT NULL,
                salt BLOB NOT NULL,
                failed_attempts INTEGER DEFAULT 0,
                last_attempt TIMESTAMP,
                locked_until TIMESTAMP,
                totp_secret BLOB
            )""")
            await db.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                action TEXT,
                details BLOB,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )""")
            await db.commit()

    async def log_action(self, user_id: int, action: str, details: Dict):
        encrypted_details = self.config.cipher_suite.encrypt(json.dumps(details).encode())
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO audit_log (user_id, action, details) VALUES (?, ?, ?)",
                (user_id, action, encrypted_details)
            )
            await db.commit()
