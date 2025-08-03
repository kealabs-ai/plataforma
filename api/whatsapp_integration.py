from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
import requests
import base64
import io
from typing import Dict, Any, List, Optional
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from database_queries.landscaping_database_query import get_client_by_whatsapp_id, create_client, update_client, get_quote_by_id, get_client_by_id

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

@router.post("/send-quote-pdf")
async def send_quote_pdf_whatsapp(
    quote_id: int = Form(..., description="ID do orçamento"),
    id_whatsapp: str = Form(..., description="ID do WhatsApp do destinatário")
):
    """Gera PDF do orçamento, retorna base64 e envia via WhatsApp"""
    try:
        # Buscar dados do orçamento
        quote = get_quote_by_id(quote_id)
        if not quote:
            raise HTTPException(status_code=404, detail="Orçamento não encontrado")
        
        # Buscar dados do cliente
        client = get_client_by_id(quote['client_id'])
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        # Gerar PDF
        pdf_buffer = generate_quote_pdf(quote, client)
        pdf_bytes = pdf_buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
        
        # Preparar body para envio via WAHA (usando modelo solicitado)
        data = {
            "session": "default",
            "chatId": id_whatsapp,
            "caption": f"Orçamento #{quote_id} - {client['client_name']}",
            "file": {
                "mimetype": "application/pdf",
                "filename": f"orcamento_{quote_id}.pdf",
                "base64": pdf_base64
            }
        }
        
        # Enviar arquivo via WAHA
        response = requests.post(
            f"{WHATSAPP_API_BASE}/sendFile",
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "PDF do orçamento enviado com sucesso.",
                "pdf_base64": pdf_base64
            }
        else:
            return {
                "success": False,
                "message": f"Erro ao enviar PDF: {response.status_code} - {response.text}",
                "pdf_base64": pdf_base64
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Erro: {str(e)}",
            "pdf_base64": None
        }

@router.post("/sendFile")
async def send_file_whatsapp(
    phone_number: str = Form(..., description="Número do destinatário em formato internacional"),
    file: UploadFile = File(..., description="Arquivo PDF a ser enviado"),
    filename: Optional[str] = Form(None, description="Nome do arquivo no WhatsApp")
):
    """Envia arquivo PDF via WhatsApp usando WAHA API"""
    try:
        # Ler conteúdo do arquivo
        file_content = await file.read()
        
        # Usar filename fornecido ou nome original do arquivo
        file_name = filename or file.filename or "documento.pdf"
        
        # Preparar dados para envio
        files = {
            'file': (file_name, file_content, file.content_type or 'application/pdf')
        }
        
        data = {
            'chatId': f"{phone_number.replace('+', '').replace('-', '').replace(' ', '')}@c.us",
            'caption': f"Documento: {file_name}"
        }
        console.log(f"Enviando arquivo para {data['chatId']} com nome {file_name}")
        # Enviar arquivo via WAHA
        response = requests.post(
            f"{WHATSAPP_API_BASE}/sendFile",
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            waha_response = response.json()
            return {
                "success": True,
                "message": "Arquivo enviado com sucesso.",
                "waha_response": waha_response
            }
        else:
            return {
                "success": False,
                "message": f"Erro ao enviar arquivo: {response.status_code}",
                "waha_response": response.text
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Erro interno: {str(e)}",
            "waha_response": None
        }

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
                id_whatsapp = contact.get("id_whatsapp")
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

def generate_quote_pdf(quote: dict, client: dict) -> io.BytesIO:
    """Gera PDF do orçamento usando ReportLab"""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    try:
        # Fundo verde
        p.setFillColor(colors.Color(0.196, 0.753, 0.212))  # #32C036
        p.rect(0, 0, width, height, fill=1)
        
        # Cabeçalho amarelo
        p.setFillColor(colors.Color(1, 0.937, 0.804))  # #FFEFCD
        p.rect(30, height-110, width-60, 80, fill=1)
        
        # Título
        p.setFillColor(colors.black)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(120, height-55, "Orçamento de Jardim")
        
        # Informações do cliente
        p.setFont("Helvetica", 10)
        p.drawString(120, height-75, f"Cliente: {client.get('client_name', '')}")
        p.drawString(420, height-75, f"Email: {client.get('email', '')}")
        p.drawString(120, height-90, f"Endereço: {client.get('address', '')}")
        p.drawString(280, height-90, f"Cidade: {client.get('city', '')} - {client.get('state', '')}")
        p.drawString(420, height-90, f"WhatsApp: {client.get('phone_number', '')}")
        
        # Corpo branco
        p.setFillColor(colors.white)
        p.rect(30, 120, width-60, height-240, fill=1)
        
        # Tabela de itens
        y_pos = height-160
        
        # Cabeçalho da tabela
        p.setFillColor(colors.Color(1, 0.937, 0.804))  # #FFEFCD
        p.rect(40, y_pos-25, width-80, 25, fill=1)
        
        p.setFillColor(colors.black)
        p.setFont("Helvetica-Bold", 11)
        p.drawString(50, y_pos-18, "Descrição")
        p.drawString(260, y_pos-18, "Qtde.")
        p.drawString(360, y_pos-18, "Preço unitário")
        p.drawString(470, y_pos-18, "Total")
        
        y_pos -= 25
        total = 0
        
        # Itens do orçamento
        items = quote.get('items', [])
        if not items:
            items = [{'description': 'Serviço de paisagismo', 'quantity': 1, 'unit_price': quote.get('total_value', 0)}]
        
        p.setFont("Helvetica", 10)
        for item in items:
            quantity = float(item.get('quantity', 1))
            unit_price = float(item.get('unit_price', 0))
            subtotal = quantity * unit_price
            total += subtotal
            
            description = str(item.get('description', item.get('service_name', 'Serviço')))[:30]
            
            p.drawString(50, y_pos-18, description)
            p.drawString(260, y_pos-18, str(int(quantity)))
            p.drawString(360, y_pos-18, f"R$ {unit_price:.2f}")
            p.drawString(470, y_pos-18, f"R$ {subtotal:.2f}")
            
            y_pos -= 25
        
        # Total geral
        p.setFillColor(colors.Color(0.549, 0.733, 0.420))  # #8CBB6B
        p.rect(40, y_pos-25, width-80, 25, fill=1)
        
        p.setFillColor(colors.black)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(320, y_pos-18, "Total do Orçamento:")
        p.drawString(470, y_pos-18, f"R$ {total:.2f}")
        
        # Rodapé
        p.setFillColor(colors.white)
        p.setFont("Helvetica", 10)
        footer_y = 80
        
        # Centralizar texto manualmente
        company_text = "KOGNIA PAISAGISMO"
        address_text = "Endereço: Rua das Flores, 123 - São Paulo - SP"
        site_text = "Site: www.kogniapaisagismo.com.br | Email: contato@kogniapaisagismo.com.br"
        phone_text = "Telefone: (11) 3333-4444 | WhatsApp: (11) 99999-8888"
        
        p.drawString((width - p.stringWidth(company_text))/2, footer_y, company_text)
        p.drawString((width - p.stringWidth(address_text))/2, footer_y-15, address_text)
        p.drawString((width - p.stringWidth(site_text))/2, footer_y-30, site_text)
        p.drawString((width - p.stringWidth(phone_text))/2, footer_y-45, phone_text)
        
        p.save()
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        # Retornar PDF simples em caso de erro
        p.setFillColor(colors.black)
        p.setFont("Helvetica", 12)
        p.drawString(100, height-100, f"Orçamento #{quote.get('id', 'N/A')}")
        p.drawString(100, height-120, f"Cliente: {client.get('client_name', 'N/A')}")
        p.drawString(100, height-140, f"Total: R$ {quote.get('total_value', 0):.2f}")
        p.save()
        buffer.seek(0)
        return buffer

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

