from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date

# Modelos para Projetos de Paisagismo
class ProjectBase(BaseModel):
    name: str = Field(..., description="Nome do projeto")
    client_name: str = Field(..., description="Nome do cliente")
    area_m2: float = Field(..., description="Área do projeto em metros quadrados")
    location: str = Field(..., description="Localização do projeto")
    start_date: date = Field(..., description="Data de início do projeto")
    end_date: Optional[date] = Field(None, description="Data de término prevista do projeto")
    budget: Optional[float] = Field(None, description="Orçamento do projeto")
    status: str = Field("planejamento", description="Status do projeto (planejamento, em_andamento, concluído, cancelado)")
    description: Optional[str] = Field(None, description="Descrição detalhada do projeto")

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nome do projeto")
    client_name: Optional[str] = Field(None, description="Nome do cliente")
    area_m2: Optional[float] = Field(None, description="Área do projeto em metros quadrados")
    location: Optional[str] = Field(None, description="Localização do projeto")
    start_date: Optional[date] = Field(None, description="Data de início do projeto")
    end_date: Optional[date] = Field(None, description="Data de término prevista do projeto")
    budget: Optional[float] = Field(None, description="Orçamento do projeto")
    status: Optional[str] = Field(None, description="Status do projeto")
    description: Optional[str] = Field(None, description="Descrição detalhada do projeto")

class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Modelos para Fornecedores de Paisagismo
class SupplierBase(BaseModel):
    name: str = Field(..., description="Nome do fornecedor")
    contact_person: str = Field(..., description="Pessoa de contato")
    phone: str = Field(..., description="Telefone de contato")
    email: str = Field(..., description="Email de contato")
    products: str = Field(..., description="Produtos fornecidos")
    last_contract: Optional[date] = Field(None, description="Data do último contrato")
    status: str = Field("Ativo", description="Status do fornecedor (Ativo, Inativo)")
    notes: Optional[str] = Field(None, description="Observações adicionais")

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nome do fornecedor")
    contact_person: Optional[str] = Field(None, description="Pessoa de contato")
    phone: Optional[str] = Field(None, description="Telefone de contato")
    email: Optional[str] = Field(None, description="Email de contato")
    products: Optional[str] = Field(None, description="Produtos fornecidos")
    last_contract: Optional[date] = Field(None, description="Data do último contrato")
    status: Optional[str] = Field(None, description="Status do fornecedor")
    notes: Optional[str] = Field(None, description="Observações adicionais")

class SupplierResponse(SupplierBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Modelos para Serviços de Paisagismo
class ServiceBase(BaseModel):
    service_name: str = Field(..., description="Nome do serviço")
    category: str = Field(..., description="Categoria do serviço")
    description: str = Field(..., description="Descrição do serviço")
    average_duration: float = Field(..., description="Duração média em horas")
    base_price: float = Field(..., description="Preço base do serviço")
    status: str = Field("Ativo", description="Status do serviço (Ativo, Inativo)")

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    service_name: Optional[str] = Field(None, description="Nome do serviço")
    category: Optional[str] = Field(None, description="Categoria do serviço")
    description: Optional[str] = Field(None, description="Descrição do serviço")
    average_duration: Optional[float] = Field(None, description="Duração média em horas")
    base_price: Optional[float] = Field(None, description="Preço base do serviço")
    status: Optional[str] = Field(None, description="Status do serviço")

class ServiceResponse(ServiceBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Modelos para Orçamentos de Paisagismo
class QuoteItemBase(BaseModel):
    service_id: int = Field(..., description="ID do serviço")
    quantity: int = Field(1, description="Quantidade")
    unit_price: float = Field(..., description="Preço unitário")
    subtotal: float = Field(..., description="Subtotal do item")
    description: Optional[str] = Field(None, description="Descrição adicional")

class QuoteBase(BaseModel):
    client_id: int = Field(..., description="ID do cliente")
    description: str = Field(..., description="Descrição do orçamento")
    created_at: Optional[date] = Field(None, description="Data de criação")
    valid_until: date = Field(..., description="Data de validade")
    total_value: float = Field(..., description="Valor total do orçamento")
    notes: Optional[str] = Field(None, description="Observações adicionais")
    status: str = Field("Pendente", description="Status do orçamento (Pendente, Aprovado, Rejeitado, Expirado)")
    items: List[QuoteItemBase] = Field(..., description="Itens do orçamento")

class QuoteCreate(QuoteBase):
    user_id: int = Field(..., description="ID do usuário")

class QuoteUpdate(BaseModel):
    client_id: Optional[int] = Field(None, description="ID do cliente")
    description: Optional[str] = Field(None, description="Descrição do orçamento")
    valid_until: Optional[date] = Field(None, description="Data de validade")
    total_value: Optional[float] = Field(None, description="Valor total do orçamento")
    notes: Optional[str] = Field(None, description="Observações adicionais")
    status: Optional[str] = Field(None, description="Status do orçamento")
    items: Optional[List[QuoteItemBase]] = Field(None, description="Itens do orçamento")

class QuoteResponse(BaseModel):
    id: int
    user_id: int
    client_id: int
    description: str
    created_at: str
    valid_until: str
    total_value: float
    status: str
    notes: Optional[str] = None
    items: List[QuoteItemBase]
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True

# Modelos para Manutenção de Paisagismo
class MaintenanceBase(BaseModel):
    project_id: int = Field(..., description="ID do projeto relacionado")
    date: date = Field(..., description="Data da manutenção")
    type: str = Field(..., description="Tipo de manutenção (poda, irrigação, adubação, etc)")
    description: str = Field(..., description="Descrição da manutenção realizada")
    cost: Optional[float] = Field(None, description="Custo da manutenção")
    duration_hours: Optional[float] = Field(None, description="Duração da manutenção em horas")
    status: str = Field("concluído", description="Status da manutenção (agendada, em_andamento, concluído, cancelada)")
    notes: Optional[str] = Field(None, description="Observações adicionais")

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(BaseModel):
    project_id: Optional[int] = Field(None, description="ID do projeto relacionado")
    date: Optional[date] = Field(None, description="Data da manutenção")
    type: Optional[str] = Field(None, description="Tipo de manutenção")
    description: Optional[str] = Field(None, description="Descrição da manutenção realizada")
    cost: Optional[float] = Field(None, description="Custo da manutenção")
    duration_hours: Optional[float] = Field(None, description="Duração da manutenção em horas")
    status: Optional[str] = Field(None, description="Status da manutenção")
    notes: Optional[str] = Field(None, description="Observações adicionais")

class MaintenanceResponse(MaintenanceBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Modelos para Clientes de Paisagismo
class ClientBase(BaseModel):
    client_name: str = Field(..., description="Nome do cliente")
    contact_person: Optional[str] = Field(None, description="Pessoa de contato")
    email: Optional[str] = Field(None, description="Email do cliente")
    phone_number: Optional[str] = Field(None, description="Número de telefone")
    address: Optional[str] = Field(None, description="Endereço")
    city: Optional[str] = Field(None, description="Cidade")
    state: Optional[str] = Field(None, description="Estado")
    zip_code: Optional[str] = Field(None, description="CEP")
    client_type: Optional[str] = Field(None, description="Tipo do cliente")
    industry: Optional[str] = Field(None, description="Setor/Indústria")
    status: str = Field("Lead", description="Status do cliente")
    last_interaction_date: Optional[date] = Field(None, description="Data da última interação")
    next_follow_up_date: Optional[date] = Field(None, description="Data do próximo follow-up")
    notes: Optional[str] = Field(None, description="Observações")
    id_whatsapp: Optional[str] = Field(None, description="ID do WhatsApp")
    img_profile: Optional[str] = Field(None, description="URL da imagem de perfil")

class ClientCreate(BaseModel):
    user_id: int = Field(..., description="ID do usuário")
    client_name: str = Field(..., description="Nome do cliente")
    contact_person: Optional[str] = Field(None, description="Pessoa de contato")
    email: Optional[str] = Field(None, description="Email do cliente")
    phone_number: Optional[str] = Field(None, description="Número de telefone")
    address: Optional[str] = Field(None, description="Endereço")
    city: Optional[str] = Field(None, description="Cidade")
    state: Optional[str] = Field(None, description="Estado")
    zip_code: Optional[str] = Field(None, description="CEP")
    client_type: Optional[str] = Field(None, description="Tipo do cliente")
    industry: Optional[str] = Field(None, description="Setor/Indústria")
    status: str = Field("Lead", description="Status do cliente")
    last_interaction_date: Optional[date] = Field(None, description="Data da última interação")
    next_follow_up_date: Optional[date] = Field(None, description="Data do próximo follow-up")
    notes: Optional[str] = Field(None, description="Observações")
    id_whatsapp: Optional[str] = Field(None, description="ID do WhatsApp")
    img_profile: Optional[str] = Field(None, description="URL da imagem de perfil")

class ClientUpdate(BaseModel):
    client_name: Optional[str] = Field(None, description="Nome do cliente")
    contact_person: Optional[str] = Field(None, description="Pessoa de contato")
    email: Optional[str] = Field(None, description="Email do cliente")
    phone_number: Optional[str] = Field(None, description="Número de telefone")
    address: Optional[str] = Field(None, description="Endereço")
    city: Optional[str] = Field(None, description="Cidade")
    state: Optional[str] = Field(None, description="Estado")
    zip_code: Optional[str] = Field(None, description="CEP")
    client_type: Optional[str] = Field(None, description="Tipo do cliente")
    industry: Optional[str] = Field(None, description="Setor/Indústria")
    status: Optional[str] = Field(None, description="Status do cliente")
    last_interaction_date: Optional[date] = Field(None, description="Data da última interação")
    next_follow_up_date: Optional[date] = Field(None, description="Data do próximo follow-up")
    notes: Optional[str] = Field(None, description="Observações")
    id_whatsapp: Optional[str] = Field(None, description="ID do WhatsApp")
    img_profile: Optional[str] = Field(None, description="URL da imagem de perfil")

class ClientResponse(ClientBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

class ClientPaginatedResponse(BaseModel):
    items: List[ClientResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int

# Modelo para respostas paginadas
class PaginatedResponse(BaseModel):
    items: List[Dict[str, Any]]
    page: int
    page_size: int
    total_items: int
    total_pages: int