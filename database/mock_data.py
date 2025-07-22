"""
Módulo para fornecer dados mockados para os endpoints de floricultura e paisagismo.
Usado temporariamente até que o banco de dados esteja configurado.
"""

# Dados mockados para floricultura
MOCK_FLOWERS = [
    {
        "id": 1,
        "user_id": 1,
        "species": "Rosa Vermelha",
        "variety": "Gallica",
        "planting_date": "2023-10-15",
        "area_m2": 25.5,
        "greenhouse_id": 1,
        "expected_harvest_date": "2024-01-15",
        "status": "active",
        "notes": "Rosa vermelha tradicional, perfeita para jardins e arranjos.",
        "created_at": "2023-10-15T10:00:00",
        "updated_at": "2023-10-15T10:00:00",
        "image_url": "https://images.unsplash.com/photo-1559563362-c667ba5f5480"
    },
    {
        "id": 2,
        "user_id": 1,
        "species": "Orquídea Phalaenopsis",
        "variety": "Branca",
        "planting_date": "2023-09-20",
        "area_m2": 10.0,
        "greenhouse_id": 2,
        "expected_harvest_date": "2024-02-20",
        "status": "active",
        "notes": "Orquídea elegante de fácil cultivo, ideal para ambientes internos.",
        "created_at": "2023-09-20T14:30:00",
        "updated_at": "2023-09-20T14:30:00",
        "image_url": "https://images.unsplash.com/photo-1566550747935-a6f55a696122"
    },
    {
        "id": 3,
        "user_id": 1,
        "species": "Lírio",
        "variety": "Asiático",
        "planting_date": "2023-11-05",
        "area_m2": 15.0,
        "greenhouse_id": 1,
        "expected_harvest_date": "2024-03-05",
        "status": "active",
        "notes": "Lírio perfumado, excelente para arranjos florais.",
        "created_at": "2023-11-05T09:15:00",
        "updated_at": "2023-11-05T09:15:00",
        "image_url": "https://images.unsplash.com/photo-1588701107566-af76b932e2e8"
    },
    {
        "id": 4,
        "user_id": 1,
        "species": "Suculenta Echeveria",
        "variety": "Elegans",
        "planting_date": "2023-08-10",
        "area_m2": 5.0,
        "greenhouse_id": 3,
        "expected_harvest_date": "2024-01-10",
        "status": "active",
        "notes": "Suculenta de baixa manutenção, perfeita para iniciantes.",
        "created_at": "2023-08-10T11:45:00",
        "updated_at": "2023-08-10T11:45:00",
        "image_url": "https://images.unsplash.com/photo-1509423350716-97f9360b4e09"
    },
    {
        "id": 5,
        "user_id": 1,
        "species": "Tulipa",
        "variety": "Vermelha",
        "planting_date": "2023-10-25",
        "area_m2": 20.0,
        "greenhouse_id": 2,
        "expected_harvest_date": "2024-02-25",
        "status": "active",
        "notes": "Tulipa colorida, ideal para canteiros e vasos.",
        "created_at": "2023-10-25T16:20:00",
        "updated_at": "2023-10-25T16:20:00",
        "image_url": "https://images.unsplash.com/photo-1589994160839-163cd867cfe8"
    },
    {
        "id": 6,
        "user_id": 1,
        "species": "Violeta",
        "variety": "Saintpaulia",
        "planting_date": "2023-09-15",
        "area_m2": 8.0,
        "greenhouse_id": 3,
        "expected_harvest_date": "2024-01-15",
        "status": "active",
        "notes": "Violeta delicada, perfeita para decoração de interiores.",
        "created_at": "2023-09-15T13:10:00",
        "updated_at": "2023-09-15T13:10:00",
        "image_url": "https://images.unsplash.com/photo-1615213612138-4d1195b8f8d0"
    }
]

MOCK_GREENHOUSES = [
    {
        "id": 1,
        "user_id": 1,
        "name": "Estufa Principal",
        "area_m2": 100.0,
        "type": "Vidro",
        "temperature_control": True,
        "humidity_control": True,
        "irrigation_system": True,
        "location": "Setor Norte",
        "notes": "Estufa principal para flores delicadas",
        "created_at": "2023-01-10T08:00:00",
        "updated_at": "2023-01-10T08:00:00"
    },
    {
        "id": 2,
        "user_id": 1,
        "name": "Estufa Secundária",
        "area_m2": 75.0,
        "type": "Policarbonato",
        "temperature_control": True,
        "humidity_control": False,
        "irrigation_system": True,
        "location": "Setor Leste",
        "notes": "Estufa para flores resistentes",
        "created_at": "2023-02-15T09:30:00",
        "updated_at": "2023-02-15T09:30:00"
    },
    {
        "id": 3,
        "user_id": 1,
        "name": "Estufa de Suculentas",
        "area_m2": 50.0,
        "type": "Acrílico",
        "temperature_control": False,
        "humidity_control": False,
        "irrigation_system": True,
        "location": "Setor Sul",
        "notes": "Estufa especializada para suculentas e cactos",
        "created_at": "2023-03-20T10:45:00",
        "updated_at": "2023-03-20T10:45:00"
    }
]

MOCK_FLORICULTURE_SUPPLIERS = [
    {
        "id": 1,
        "user_id": 1,
        "name": "Flores & Cia",
        "contact_person": "João Silva",
        "phone": "(11) 98765-4321",
        "email": "contato@floresecia.com.br",
        "products": "Flores, Sementes, Mudas",
        "last_purchase": "2023-08-15",
        "status": "Ativo",
        "notes": "Fornecedor principal de sementes",
        "created_at": "2023-01-05T08:00:00",
        "updated_at": "2023-08-15T14:30:00"
    },
    {
        "id": 2,
        "user_id": 1,
        "name": "Jardim Verde",
        "contact_person": "Maria Oliveira",
        "phone": "(11) 91234-5678",
        "email": "vendas@jardimverde.com.br",
        "products": "Vasos, Substratos, Fertilizantes",
        "last_purchase": "2023-09-02",
        "status": "Ativo",
        "notes": "Fornecedor de insumos para cultivo",
        "created_at": "2023-02-10T09:15:00",
        "updated_at": "2023-09-02T11:20:00"
    },
    {
        "id": 3,
        "user_id": 1,
        "name": "Sementes Premium",
        "contact_person": "Carlos Santos",
        "phone": "(11) 97777-8888",
        "email": "carlos@sementespremium.com.br",
        "products": "Sementes, Mudas",
        "last_purchase": "2023-07-20",
        "status": "Inativo",
        "notes": "Fornecedor de sementes importadas",
        "created_at": "2023-03-15T10:30:00",
        "updated_at": "2023-07-20T16:45:00"
    }
]

# Dados mockados para paisagismo
MOCK_LANDSCAPING_PROJECTS = [
    {
        "id": 1,
        "user_id": 1,
        "name": "Jardim Residencial Silva",
        "client_name": "Família Silva",
        "area_m2": 150.0,
        "location": "Rua das Flores, 123",
        "start_date": "2023-09-10",
        "end_date": "2023-11-15",
        "budget": 15000.0,
        "status": "concluído",
        "description": "Projeto de jardim residencial com área de lazer",
        "created_at": "2023-09-01T09:00:00",
        "updated_at": "2023-11-15T16:30:00"
    },
    {
        "id": 2,
        "user_id": 1,
        "name": "Praça Central",
        "client_name": "Prefeitura Municipal",
        "area_m2": 500.0,
        "location": "Centro da Cidade",
        "start_date": "2023-10-05",
        "end_date": "2024-02-28",
        "budget": 50000.0,
        "status": "em_andamento",
        "description": "Revitalização da praça central com novo paisagismo",
        "created_at": "2023-09-20T14:00:00",
        "updated_at": "2023-12-10T11:45:00"
    },
    {
        "id": 3,
        "user_id": 1,
        "name": "Condomínio Jardins",
        "client_name": "Condomínio Jardins",
        "area_m2": 800.0,
        "location": "Av. das Palmeiras, 1000",
        "start_date": "2024-03-01",
        "end_date": "2024-06-30",
        "budget": 75000.0,
        "status": "planejamento",
        "description": "Projeto completo de paisagismo para condomínio de luxo",
        "created_at": "2023-12-15T10:30:00",
        "updated_at": "2023-12-15T10:30:00"
    }
]

MOCK_LANDSCAPING_SUPPLIERS = [
    {
        "id": 1,
        "user_id": 1,
        "name": "Pedras & Jardins",
        "contact_person": "Roberto Almeida",
        "phone": "(11) 99876-5432",
        "email": "contato@pedrasejardins.com.br",
        "products": "Pedras decorativas, Cascalho, Areia",
        "last_contract": "2023-10-15",
        "status": "Ativo",
        "notes": "Fornecedor de materiais para pavimentação",
        "created_at": "2023-05-10T08:30:00",
        "updated_at": "2023-10-15T14:20:00"
    },
    {
        "id": 2,
        "user_id": 1,
        "name": "Árvores Brasil",
        "contact_person": "Ana Ferreira",
        "phone": "(11) 98765-1234",
        "email": "vendas@arvoresbrasil.com.br",
        "products": "Árvores, Arbustos, Palmeiras",
        "last_contract": "2023-11-20",
        "status": "Ativo",
        "notes": "Fornecedor especializado em árvores nativas",
        "created_at": "2023-06-15T09:45:00",
        "updated_at": "2023-11-20T11:30:00"
    },
    {
        "id": 3,
        "user_id": 1,
        "name": "Irrigação Moderna",
        "contact_person": "Paulo Mendes",
        "phone": "(11) 97654-3210",
        "email": "paulo@irrigacaomoderna.com.br",
        "products": "Sistemas de irrigação, Aspersores, Controladores",
        "last_contract": "2023-08-05",
        "status": "Ativo",
        "notes": "Fornecedor de sistemas de irrigação automatizados",
        "created_at": "2023-07-20T10:15:00",
        "updated_at": "2023-08-05T15:40:00"
    }
]

MOCK_LANDSCAPING_SERVICES = [
    {
        "id": 1,
        "user_id": 1,
        "service_name": "Projeto de Jardim",
        "category": "Projeto",
        "description": "Elaboração de projeto paisagístico completo",
        "average_duration": 20.0,
        "base_price": 2500.0,
        "status": "Ativo",
        "created_at": "2023-01-15T09:00:00",
        "updated_at": "2023-01-15T09:00:00"
    },
    {
        "id": 2,
        "user_id": 1,
        "service_name": "Plantio de Árvores",
        "category": "Plantio",
        "description": "Serviço de plantio de árvores de médio porte",
        "average_duration": 4.0,
        "base_price": 350.0,
        "status": "Ativo",
        "created_at": "2023-01-15T09:15:00",
        "updated_at": "2023-01-15T09:15:00"
    },
    {
        "id": 3,
        "user_id": 1,
        "service_name": "Instalação de Gramado",
        "category": "Instalação",
        "description": "Preparação do solo e instalação de grama em placas",
        "average_duration": 8.0,
        "base_price": 15.0,
        "status": "Ativo",
        "created_at": "2023-01-15T09:30:00",
        "updated_at": "2023-01-15T09:30:00"
    },
    {
        "id": 4,
        "user_id": 1,
        "service_name": "Manutenção Mensal",
        "category": "Manutenção",
        "description": "Serviço mensal de manutenção de jardins",
        "average_duration": 6.0,
        "base_price": 800.0,
        "status": "Ativo",
        "created_at": "2023-01-15T09:45:00",
        "updated_at": "2023-01-15T09:45:00"
    },
    {
        "id": 5,
        "user_id": 1,
        "service_name": "Poda de Árvores",
        "category": "Manutenção",
        "description": "Serviço especializado de poda e modelagem de árvores",
        "average_duration": 5.0,
        "base_price": 450.0,
        "status": "Ativo",
        "created_at": "2023-01-15T10:00:00",
        "updated_at": "2023-01-15T10:00:00"
    }
]

MOCK_LANDSCAPING_QUOTES = [
    {
        "id": 1,
        "user_id": 1,
        "client": "Família Silva",
        "description": "Orçamento para jardim residencial",
        "created_date": "2023-09-01",
        "valid_until": "2023-10-01",
        "total_value": 12500.0,
        "status": "Aprovado",
        "created_at": "2023-09-01T09:00:00",
        "updated_at": "2023-09-10T14:30:00",
        "items": [
            {
                "service_id": 1,
                "quantity": 1,
                "unit_price": 2500.0,
                "description": "Projeto paisagístico completo"
            },
            {
                "service_id": 2,
                "quantity": 5,
                "unit_price": 350.0,
                "description": "Plantio de árvores frutíferas"
            },
            {
                "service_id": 3,
                "quantity": 150,
                "unit_price": 15.0,
                "description": "Instalação de grama esmeralda"
            }
        ]
    },
    {
        "id": 2,
        "user_id": 1,
        "client": "Condomínio Jardins",
        "description": "Orçamento para paisagismo do condomínio",
        "created_date": "2023-12-15",
        "valid_until": "2024-01-15",
        "total_value": 75000.0,
        "status": "Pendente",
        "created_at": "2023-12-15T10:30:00",
        "updated_at": "2023-12-15T10:30:00",
        "items": [
            {
                "service_id": 1,
                "quantity": 1,
                "unit_price": 5000.0,
                "description": "Projeto paisagístico para condomínio"
            },
            {
                "service_id": 2,
                "quantity": 20,
                "unit_price": 400.0,
                "description": "Plantio de árvores de grande porte"
            },
            {
                "service_id": 3,
                "quantity": 800,
                "unit_price": 15.0,
                "description": "Instalação de grama em áreas comuns"
            },
            {
                "service_id": 4,
                "quantity": 12,
                "unit_price": 3000.0,
                "description": "Contrato anual de manutenção"
            }
        ]
    },
    {
        "id": 3,
        "user_id": 1,
        "client": "Prefeitura Municipal",
        "description": "Orçamento para revitalização da praça central",
        "created_date": "2023-09-20",
        "valid_until": "2023-10-20",
        "total_value": 45000.0,
        "status": "Aprovado",
        "created_at": "2023-09-20T14:00:00",
        "updated_at": "2023-10-05T11:15:00",
        "items": [
            {
                "service_id": 1,
                "quantity": 1,
                "unit_price": 4000.0,
                "description": "Projeto de revitalização da praça"
            },
            {
                "service_id": 2,
                "quantity": 15,
                "unit_price": 500.0,
                "description": "Plantio de árvores nativas"
            },
            {
                "service_id": 3,
                "quantity": 500,
                "unit_price": 15.0,
                "description": "Instalação de grama em áreas de lazer"
            },
            {
                "service_id": 5,
                "quantity": 10,
                "unit_price": 450.0,
                "description": "Poda de árvores existentes"
            }
        ]
    }
]

MOCK_LANDSCAPING_MAINTENANCE = [
    {
        "id": 1,
        "user_id": 1,
        "project_id": 1,
        "date": "2023-11-20",
        "type": "Poda",
        "description": "Poda de arbustos e modelagem de cercas vivas",
        "cost": 350.0,
        "duration_hours": 4.5,
        "status": "concluído",
        "notes": "Cliente satisfeito com o resultado",
        "created_at": "2023-11-20T09:00:00",
        "updated_at": "2023-11-20T14:30:00",
        "project_name": "Jardim Residencial Silva"
    },
    {
        "id": 2,
        "user_id": 1,
        "project_id": 1,
        "date": "2023-12-20",
        "type": "Irrigação",
        "description": "Manutenção do sistema de irrigação automática",
        "cost": 250.0,
        "duration_hours": 3.0,
        "status": "concluído",
        "notes": "Substituição de aspersores danificados",
        "created_at": "2023-12-20T10:15:00",
        "updated_at": "2023-12-20T13:45:00",
        "project_name": "Jardim Residencial Silva"
    },
    {
        "id": 3,
        "user_id": 1,
        "project_id": 2,
        "date": "2023-11-15",
        "type": "Plantio",
        "description": "Plantio de flores sazonais nos canteiros",
        "cost": 1200.0,
        "duration_hours": 8.0,
        "status": "concluído",
        "notes": "Plantio de 500 mudas de flores variadas",
        "created_at": "2023-11-15T08:30:00",
        "updated_at": "2023-11-15T17:30:00",
        "project_name": "Praça Central"
    },
    {
        "id": 4,
        "user_id": 1,
        "project_id": 2,
        "date": "2023-12-15",
        "type": "Adubação",
        "description": "Adubação de canteiros e árvores",
        "cost": 800.0,
        "duration_hours": 6.0,
        "status": "concluído",
        "notes": "Aplicação de adubo orgânico e fertilizante NPK",
        "created_at": "2023-12-15T09:00:00",
        "updated_at": "2023-12-15T16:00:00",
        "project_name": "Praça Central"
    },
    {
        "id": 5,
        "user_id": 1,
        "project_id": 2,
        "date": "2024-01-15",
        "type": "Poda",
        "description": "Poda de formação em árvores jovens",
        "cost": 1500.0,
        "duration_hours": 10.0,
        "status": "agendada",
        "notes": "Agendado com a secretaria de obras",
        "created_at": "2023-12-20T11:30:00",
        "updated_at": "2023-12-20T11:30:00",
        "project_name": "Praça Central"
    }
]