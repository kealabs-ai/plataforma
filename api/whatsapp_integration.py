from fastapi import APIRouter, HTTPException, Query
import requests
import base64
from typing import Dict, Any, List
from database_queries.landscaping_database_query import get_client_by_whatsapp_id, create_client, update_client

router = APIRouter(
    prefix="/api/whatsapp",
    tags=["WhatsApp Integration"],
    responses={404: {"description": "Not found"}},
)
print("chegou aqui!")
WHATSAPP_API_BASE = "http://waha:3000/api"

@router.get("/test")
async def test_whatsapp_integration():
    """Endpoint de teste para verificar se a integração está funcionando"""
    return {"status": "ok", "message": "WhatsApp integration is working"}

@router.post("/webhook")
async def whatsapp_webhook(data: dict):
    """Webhook para receber eventos do WhatsApp"""
    return data

@router.post("/sync-contacts")
async def sync_whatsapp_contacts(user_id: int = Query(..., description="ID do usuário")):
    """
    Sincroniza contatos do WhatsApp com a tabela landscaping_crm_clients
    """
    print(f"Iniciando sincronização para user_id: {user_id}")
    
    try:
        # Tentar conectar com WhatsApp API
        print(f"Tentando conectar com {WHATSAPP_API_BASE}/contacts/all")
        response = requests.get(f"{WHATSAPP_API_BASE}/contacts/all", timeout=5000)
        response.raise_for_status()
        contacts = response.json()
        print(f"Recebidos {len(contacts)} contatos do WhatsApp")
        
        # Filtrar contatos válidos
        valid_contacts = []
        for contact in contacts:
            if (contact.get("isUser") == True and 
                contact.get("isGroup") == False and 
                contact.get("isWAContact") == True and 
                contact.get("isMyContact") == True and 
                contact.get("isBlocked") == False):
                valid_contacts.append(contact)
        
        print(f"Encontrados {len(valid_contacts)} contatos válidos")
        synced_count = 0
        errors = []
        
        for contact in valid_contacts:
            try:
                id_whatsapp = contact.get("id")
                phone_number = contact.get("number")
                client_name = contact.get("name", "")
                contact_person = contact.get("pushname") or contact.get("shortName", "")

                # Buscar foto do perfil
                img_profile = None
                try:
                    response_img_profile = requests.get(
                        f"{WHATSAPP_API_BASE}/contacts/profile-picture?contactId={id_whatsapp}",
                        timeout=10
                    )
                    if response_img_profile.status_code == 200:
                        img_data = response_img_profile.json()
                        img_profile = img_data.get("profilePictureURL")
                        print(f"Foto encontrada para {client_name}: {img_profile}")
                except Exception as img_error:
                    print(f"Erro ao buscar foto de {client_name}: {img_error}")

                # Verificar se já existe
                existing_client = get_client_by_whatsapp_id(id_whatsapp)
                if existing_client:
                    update_data = {
                        "phone_number": phone_number,
                        "client_name": client_name,
                        "contact_person": contact_person
                    }
                    if img_profile:
                        update_data["img_profile"] = img_profile
                    update_client(existing_client["id"], user_id, update_data)
                else:
                    new_client = create_client(
                        user_id=user_id,
                        client_name=client_name,
                        contact_person=contact_person,
                        phone_number=phone_number,
                        status="Lead",
                        id_whatsapp=id_whatsapp,
                        img_profile=img_profile
                    )
                    if new_client:
                        synced_count += 1
                        
            except Exception as contact_error:
                print(f"Erro ao processar contato: {contact_error}")
                errors.append(str(contact_error))
        
        return {
            "message": f"Sincronização concluída. {synced_count} contatos sincronizados.",
            "total_contacts": len(valid_contacts),
            "processed_count": len(valid_contacts),
            "synced_count": synced_count,
            "errors": errors
        }
        
    except requests.RequestException as e:
        print(f"Erro de conexão com WhatsApp: {e}")
        return create_mock_contacts(user_id)
    except Exception as e:
        print(f"Erro geral na sincronização: {e}")
        return create_mock_contacts(user_id)

def create_mock_contacts(user_id: int) -> Dict[str, Any]:
    """
    Cria contatos mockados para teste quando WhatsApp não está disponível
    """
    print(f"Criando contatos mockados para user_id: {user_id}")
    
    mock_contacts = [
        {"id": "5511999999999@c.us", "name": "João Silva", "pushname": "João", "number": "5511999999999"},
        {"id": "5511888888888@c.us", "name": "Maria Santos", "pushname": "Maria", "number": "5511888888888"},
        {"id": "5511777777777@c.us", "name": "Pedro Costa", "pushname": "Pedro", "number": "5511777777777"}
    ]
    
    synced_count = 0
    errors = []
    
    try:
        for contact in mock_contacts:
            try:
                existing_client = get_client_by_whatsapp_id(contact["id"])
                
                if not existing_client:
                    new_client = create_client(
                        user_id=user_id,
                        client_name=contact["name"],
                        contact_person=contact["pushname"],
                        phone_number=contact["number"],
                        status="Lead",
                        id_whatsapp=contact["id"]
                    )
                    if new_client:
                        synced_count += 1
                        print(f"Cliente mockado criado: {contact['name']}")
                else:
                    print(f"Cliente já existe: {contact['name']}")
                    
            except Exception as e:
                error_msg = f"Erro ao criar {contact['name']}: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
                
    except Exception as e:
        print(f"Erro geral ao criar mocks: {e}")
        errors.append(str(e))
    
    return {
        "message": f"WhatsApp indisponível. {synced_count} contatos de teste foram criados.",
        "total_contacts": len(mock_contacts),
        "processed_count": len(mock_contacts),
        "synced_count": synced_count,
        "errors": errors
    }

