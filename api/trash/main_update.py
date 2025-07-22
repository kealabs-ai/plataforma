# Adicionar estas linhas após as importações de routers existentes
from floriculture_endpoints import router as floriculture_endpoints_router
from landscaping_endpoints_updated import router as landscaping_endpoints_router

# Adicionar estas linhas após os app.include_router existentes
app.include_router(floriculture_endpoints_router)
app.include_router(landscaping_endpoints_router)

# Adicionar endpoints mock para floricultura
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

# Adicionar endpoints mock para paisagismo
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