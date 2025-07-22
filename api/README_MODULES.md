# Integração dos Módulos de Floricultura e Paisagismo

Este documento descreve como integrar os novos módulos de Floricultura e Paisagismo à plataforma Kognia One.

## Arquivos Criados

### Módulos de Banco de Dados
- `backend/floriculture_db.py`: Operações CRUD para o módulo de Floricultura
- `backend/landscaping_db.py`: Operações CRUD para o módulo de Paisagismo
- `backend/auth.py`: Funções de autenticação para os endpoints

### Endpoints da API
- `api/floriculture_endpoints.py`: Endpoints para o módulo de Floricultura
- `api/landscaping_endpoints_updated.py`: Endpoints para o módulo de Paisagismo

### Esquema do Banco de Dados
- `database/floriculture_landscaping_schema.sql`: Esquema SQL para os módulos

### Frontend
- `frontend/templates/floriculture/flower_cultivation.html`: Tela para gerenciamento de cultivo de flores
- `frontend/templates/floriculture/greenhouses.html`: Tela para gerenciamento de estufas
- `frontend/templates/floriculture/dashboard.html`: Dashboard de floricultura

## Instruções de Integração

### 1. Configuração do Banco de Dados

Execute o script SQL para criar as tabelas necessárias:

```bash
mysql -u seu_usuario -p sua_senha sua_base_de_dados < database/floriculture_landscaping_schema.sql
```

### 2. Integração dos Endpoints

Adicione as seguintes linhas ao arquivo `api/main.py` após as importações de routers existentes:

```python
from floriculture_endpoints import router as floriculture_endpoints_router
from landscaping_endpoints_updated import router as landscaping_endpoints_router
```

E adicione estas linhas após os `app.include_router` existentes:

```python
app.include_router(floriculture_endpoints_router)
app.include_router(landscaping_endpoints_router)
```

### 3. Configuração do Frontend

Certifique-se de que as rotas para as novas telas estejam configuradas no arquivo `frontend/app_flask.py`:

```python
from floriculture import floriculture_bp

app.register_blueprint(floriculture_bp)
```

### 4. Endpoints Mock para Desenvolvimento

Para desenvolvimento, você pode adicionar os endpoints mock ao arquivo `api/main.py`:

```python
@app.get("/api/floriculture/dashboard/summary")
async def floriculture_dashboard_summary():
    return {
        "total_flowers_in_cultivation": 1800,
        "total_area_m2": 325.0,
        "total_greenhouses": 3,
        "total_harvest_month": 350,
        "flowers_by_species": [
            {"species": "Rosa", "quantity": 500},
            {"species": "Tulipa", "quantity": 1000},
            {"species": "Orquídea", "quantity": 300}
        ],
        "harvest_by_month": [
            {"month": "2024-06", "quantity": 350},
            {"month": "2024-07", "quantity": 450},
            {"month": "2024-08", "quantity": 400}
        ],
        "sales_by_month": [
            {"month": "2024-06", "total_value": 1450.0},
            {"month": "2024-07", "total_value": 1800.0},
            {"month": "2024-08", "total_value": 1650.0}
        ],
        "quality_distribution": [
            {"grade": "A", "percentage": 60},
            {"grade": "B", "percentage": 30},
            {"grade": "C", "percentage": 10}
        ]
    }

@app.get("/api/floriculture/greenhouses/dashboard")
async def greenhouses_dashboard():
    return {
        "greenhouses_by_type": [
            {"type": "Vidro", "count": 1},
            {"type": "Plástico", "count": 1},
            {"type": "Policarbonato", "count": 1}
        ],
        "temperature_trends": [
            {"date": "2024-04-08", "min": 18.5, "avg": 22.8, "max": 27.2},
            {"date": "2024-04-09", "min": 19.0, "avg": 23.1, "max": 26.5},
            {"date": "2024-04-10", "min": 19.5, "avg": 23.4, "max": 26.8}
        ],
        "humidity_trends": [
            {"date": "2024-04-08", "min": 60.0, "avg": 72.5, "max": 85.0},
            {"date": "2024-04-09", "min": 62.0, "avg": 73.0, "max": 84.0},
            {"date": "2024-04-10", "min": 65.0, "avg": 73.3, "max": 80.0}
        ],
        "occupancy_rate": [
            {"greenhouse_id": 1, "name": "Estufa Principal", "capacity": 500.0, "used": 450.0, "percentage": 90.0},
            {"greenhouse_id": 2, "name": "Estufa Secundária", "capacity": 300.0, "used": 250.0, "percentage": 83.3},
            {"greenhouse_id": 3, "name": "Estufa Experimental", "capacity": 150.0, "used": 100.0, "percentage": 66.7}
        ]
    }

@app.get("/api/landscaping/dashboard")
async def landscaping_dashboard():
    return {
        "projects_summary": {
            "total_projects": 10,
            "active_projects": 6,
            "completed_projects": 3,
            "cancelled_projects": 1
        },
        "projects_by_type": [
            {"type": "Residencial", "count": 5},
            {"type": "Comercial", "count": 3},
            {"type": "Público", "count": 2}
        ],
        "budget_summary": {
            "total_budget": 250000.0,
            "total_spent": 180000.0,
            "percentage": 72.0
        },
        "tasks_by_status": [
            {"status": "Pendente", "count": 15},
            {"status": "Em Andamento", "count": 22},
            {"status": "Concluída", "count": 48}
        ],
        "materials_by_category": [
            {"category": "Plantas", "total": 45000.0},
            {"category": "Materiais de Construção", "total": 65000.0},
            {"category": "Ferramentas", "total": 12000.0},
            {"category": "Outros", "total": 8000.0}
        ],
        "monthly_progress": [
            {"month": "2024-01", "completed_tasks": 12},
            {"month": "2024-02", "completed_tasks": 18},
            {"month": "2024-03", "completed_tasks": 15},
            {"month": "2024-04", "completed_tasks": 20}
        ]
    }
```

## Estrutura de Endpoints

### Floricultura

- **Cultivo de Flores**
  - `GET /api/floriculture/endpoints/flowers`: Lista todos os cultivos
  - `POST /api/floriculture/endpoints/flowers`: Cria um novo cultivo
  - `GET /api/floriculture/endpoints/flowers/{flower_id}`: Obtém um cultivo específico
  - `PUT /api/floriculture/endpoints/flowers/{flower_id}`: Atualiza um cultivo
  - `DELETE /api/floriculture/endpoints/flowers/{flower_id}`: Remove um cultivo

- **Estufas**
  - `GET /api/floriculture/endpoints/greenhouses`: Lista todas as estufas
  - `POST /api/floriculture/endpoints/greenhouses`: Cria uma nova estufa
  - `GET /api/floriculture/endpoints/greenhouses/{greenhouse_id}`: Obtém uma estufa específica
  - `PUT /api/floriculture/endpoints/greenhouses/{greenhouse_id}`: Atualiza uma estufa
  - `DELETE /api/floriculture/endpoints/greenhouses/{greenhouse_id}`: Remove uma estufa

- **Registros de Clima**
  - `POST /api/floriculture/endpoints/climate`: Cria um novo registro de clima
  - `GET /api/floriculture/endpoints/climate/{greenhouse_id}`: Obtém registros de clima para uma estufa

- **Registros de Colheita**
  - `POST /api/floriculture/endpoints/harvest`: Adiciona um novo registro de colheita
  - `GET /api/floriculture/endpoints/harvest/{flower_id}`: Obtém registros de colheita para um cultivo

- **Registros de Tratamento**
  - `POST /api/floriculture/endpoints/treatment`: Adiciona um novo registro de tratamento
  - `GET /api/floriculture/endpoints/treatment/{flower_id}`: Obtém registros de tratamento para um cultivo

- **Registros de Venda**
  - `POST /api/floriculture/endpoints/sales`: Adiciona um novo registro de venda
  - `GET /api/floriculture/endpoints/sales`: Obtém registros de venda com filtros

- **Dashboard**
  - `GET /api/floriculture/endpoints/dashboard/summary`: Obtém dados resumidos para o dashboard
  - `GET /api/floriculture/endpoints/dashboard/greenhouse`: Obtém dados para o dashboard de estufas
  - `GET /api/floriculture/endpoints/dashboard/user`: Obtém dados para o dashboard personalizado do usuário

### Paisagismo

- **Projetos**
  - `GET /api/landscaping/endpoints/projects`: Lista todos os projetos
  - `POST /api/landscaping/endpoints/projects`: Cria um novo projeto
  - `GET /api/landscaping/endpoints/projects/{project_id}`: Obtém um projeto específico
  - `PUT /api/landscaping/endpoints/projects/{project_id}`: Atualiza um projeto
  - `DELETE /api/landscaping/endpoints/projects/{project_id}`: Remove um projeto

- **Tarefas**
  - `POST /api/landscaping/endpoints/tasks`: Cria uma nova tarefa
  - `GET /api/landscaping/endpoints/tasks/project/{project_id}`: Obtém tarefas de um projeto
  - `GET /api/landscaping/endpoints/tasks/{task_id}`: Obtém uma tarefa específica
  - `PUT /api/landscaping/endpoints/tasks/{task_id}`: Atualiza uma tarefa
  - `DELETE /api/landscaping/endpoints/tasks/{task_id}`: Remove uma tarefa

- **Materiais**
  - `POST /api/landscaping/endpoints/materials`: Registra um novo material
  - `GET /api/landscaping/endpoints/materials/project/{project_id}`: Obtém materiais de um projeto
  - `GET /api/landscaping/endpoints/materials/{material_id}`: Obtém um material específico
  - `PUT /api/landscaping/endpoints/materials/{material_id}`: Atualiza um material
  - `DELETE /api/landscaping/endpoints/materials/{material_id}`: Remove um material

- **Registros de Plantio**
  - `POST /api/landscaping/endpoints/planting`: Cria um novo registro de plantio
  - `GET /api/landscaping/endpoints/planting/project/{project_id}`: Obtém registros de plantio de um projeto

- **Dashboard**
  - `GET /api/landscaping/endpoints/dashboard`: Obtém dados resumidos para o dashboard
  - `GET /api/landscaping/endpoints/dashboard/project/{project_id}`: Obtém um resumo detalhado de um projeto específico