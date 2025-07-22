from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Dict, Any
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.backend.database import get_db
from app.backend.auth import create_access_token, get_current_user
from app.backend.models import User, Token

router = APIRouter(tags=["authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para autenticação de usuários e geração de token JWT.
    
    Valida as credenciais do usuário contra o banco de dados e retorna um token de acesso
    se as credenciais forem válidas.
    """
    db = get_db()
    user = db.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera o token de acesso com validade de 30 minutos
    access_token = create_access_token(data={"sub": user.username})
    
    # Registra o login bem-sucedido no log de atividades
    try:
        db.log_activity(
            user_id=user.id,
            action="login",
            entity_type="auth",
            details={"ip": "client_ip", "timestamp": datetime.utcnow().isoformat()}
        )
    except Exception:
        # Falha no registro de log não deve impedir o login
        pass
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/validate-token")
async def validate_token(current_user: User = Depends(get_current_user)):
    """
    Endpoint para validar um token JWT existente.
    
    Retorna informações do usuário se o token for válido.
    """
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name
        }
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Endpoint para logout de usuário.
    
    Na implementação atual, o logout é gerenciado pelo cliente removendo o token.
    Este endpoint serve principalmente para registrar a ação de logout.
    """
    db = get_db()
    try:
        db.log_activity(
            user_id=current_user.id,
            action="logout",
            entity_type="auth",
            details={"timestamp": datetime.utcnow().isoformat()}
        )
    except Exception:
        pass
    
    return {"message": "Logout realizado com sucesso"}

@router.get("/user-info")
async def get_user_info(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Retorna informações detalhadas do usuário autenticado.
    """
    db = get_db()
    
    # Obtém os papéis (roles) do usuário
    user_roles = db.get_user_roles(current_user.id)
    
    # Obtém as configurações personalizadas do usuário
    user_settings = db.get_user_settings(current_user.id)
    
    return {
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at
        },
        "roles": user_roles,
        "settings": user_settings
    }