import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from passlib.context import CryptContext
from .models import UserCreate, User, UserInDB

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_HOST = os.getenv("DB_HOST", "http://localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root_password")
DB_NAME = os.getenv("DB_NAME", "kognia_one_db")

# Verifica se a porta é válida
if not DB_PORT:
    DB_PORT = "3306"

# Constrói a URL de conexão com o banco de dados
if DB_PASSWORD:
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criação do engine SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Contexto de criptografia para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Database:
    def __init__(self, session: Session):
        self.session = session
    
    def get_user_by_username(self, username: str) -> Optional[UserInDB]:
        # Implementação real usaria SQLAlchemy
        # Exemplo simplificado para demonstração
        from .models import users_table
        user_dict = self.session.query(users_table).filter(users_table.c.username == username).first()
        if user_dict:
            return UserInDB(**user_dict)
        return None
    
    def create_user(self, user: UserCreate) -> User:
        hashed_password = pwd_context.hash(user.password)
        db_user = UserInDB(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name
        )
        # Implementação real usaria SQLAlchemy
        # Exemplo simplificado para demonstração
        from .models import users_table
        self.session.execute(users_table.insert().values(**db_user.dict()))
        self.session.commit()
        return User(**db_user.dict(exclude={"hashed_password"}))
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return User(**user.dict(exclude={"hashed_password"}))

# Função para obter uma instância do banco de dados
def get_db():
    db = SessionLocal()
    try:
        return Database(db)
    finally:
        db.close()