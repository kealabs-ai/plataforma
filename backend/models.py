from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime
from datetime import datetime

# Metadados SQLAlchemy
metadata = MetaData()

# Definição das tabelas SQLAlchemy
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String(50), unique=True, index=True),
    Column("email", String(100), unique=True, index=True),
    Column("full_name", String(100)),
    Column("hashed_password", String(100)),
    Column("is_active", Boolean, default=True),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

llm_requests_table = Table(
    "llm_requests",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("model", String(50)),
    Column("prompt", String(1000)),
    Column("response", String(5000)),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("tokens_used", Integer)
)

# Modelos Pydantic para validação e serialização
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LLMRequest(BaseModel):
    prompt: str
    model: str
    options: Optional[Dict[str, Any]] = None

class LLMResponse(BaseModel):
    response: str
    model: str
    metadata: Optional[Dict[str, Any]] = None

class AgentRequest(BaseModel):
    agent_name: str
    params: Dict[str, Any]

class AgentResponse(BaseModel):
    result: Any
    agent: str
    metadata: Optional[Dict[str, Any]] = None
    
class WorkflowRequest(BaseModel):
    workflow_id: str
    data: Dict[str, Any]
    
class WorkflowResponse(BaseModel):
    execution_id: str
    status: str
    data: Optional[Dict[str, Any]] = None