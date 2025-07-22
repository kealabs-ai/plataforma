from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date

# Modelos para Cultivos de Flores
class FlowerBase(BaseModel):
    species: str = Field(..., description="Espécie da flor")
    variety: Optional[str] = Field(None, description="Variedade da flor")
    planting_date: date = Field(..., description="Data de plantio")
    area_m2: float = Field(..., description="Área de cultivo em metros quadrados")
    greenhouse_id: Optional[int] = Field(None, description="ID da estufa onde está sendo cultivada")
    expected_harvest_date: Optional[date] = Field(None, description="Data prevista para colheita")
    status: str = Field("active", description="Status do cultivo (active, harvested, failed)")
    notes: Optional[str] = Field(None, description="Observações adicionais")

class FlowerCreate(FlowerBase):
    pass

class FlowerUpdate(BaseModel):
    species: Optional[str] = Field(None, description="Espécie da flor")
    variety: Optional[str] = Field(None, description="Variedade da flor")
    planting_date: Optional[date] = Field(None, description="Data de plantio")
    area_m2: Optional[float] = Field(None, description="Área de cultivo em metros quadrados")
    greenhouse_id: Optional[int] = Field(None, description="ID da estufa onde está sendo cultivada")
    expected_harvest_date: Optional[date] = Field(None, description="Data prevista para colheita")
    status: Optional[str] = Field(None, description="Status do cultivo")
    notes: Optional[str] = Field(None, description="Observações adicionais")

class FlowerResponse(FlowerBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Modelos para Estufas
class GreenhouseBase(BaseModel):
    name: str = Field(..., description="Nome da estufa")
    area_m2: float = Field(..., description="Área da estufa em metros quadrados")
    type: str = Field(..., description="Tipo de estufa")
    temperature_control: bool = Field(False, description="Possui controle de temperatura")
    humidity_control: bool = Field(False, description="Possui controle de umidade")
    irrigation_system: bool = Field(False, description="Possui sistema de irrigação")
    location: Optional[str] = Field(None, description="Localização da estufa")
    notes: Optional[str] = Field(None, description="Observações adicionais")

class GreenhouseCreate(GreenhouseBase):
    pass

class GreenhouseUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nome da estufa")
    area_m2: Optional[float] = Field(None, description="Área da estufa em metros quadrados")
    type: Optional[str] = Field(None, description="Tipo de estufa")
    temperature_control: Optional[bool] = Field(None, description="Possui controle de temperatura")
    humidity_control: Optional[bool] = Field(None, description="Possui controle de umidade")
    irrigation_system: Optional[bool] = Field(None, description="Possui sistema de irrigação")
    location: Optional[str] = Field(None, description="Localização da estufa")
    notes: Optional[str] = Field(None, description="Observações adicionais")

class GreenhouseResponse(GreenhouseBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Modelos para Fornecedores
class SupplierBase(BaseModel):
    name: str = Field(..., description="Nome do fornecedor")
    contact_person: str = Field(..., description="Pessoa de contato")
    phone: str = Field(..., description="Telefone de contato")
    email: str = Field(..., description="Email de contato")
    products: str = Field(..., description="Produtos fornecidos")
    last_purchase: Optional[date] = Field(None, description="Data da última compra")
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
    last_purchase: Optional[date] = Field(None, description="Data da última compra")
    status: Optional[str] = Field(None, description="Status do fornecedor")
    notes: Optional[str] = Field(None, description="Observações adicionais")

class SupplierResponse(SupplierBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Modelo para respostas paginadas
class PaginatedResponse(BaseModel):
    items: List[Dict[str, Any]]
    page: int
    page_size: int
    total_items: int
    total_pages: int