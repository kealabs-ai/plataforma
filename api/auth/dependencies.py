from datetime import datetime
from typing import Optional

# Definição mínima da classe User
class User:
    def __init__(self, id: int, username: str, email: str, name: str):
        self.id = id
        self.username = username
        self.email = email
        self.name = name
        self.is_active = True
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

async def get_current_user():
    """Função simplificada para autenticação que retorna um usuário demo."""
    return User(
        id=1,
        username="demo",
        email="demo@example.com",
        name="Demo User"
    )