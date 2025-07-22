from typing import Dict, List, Any, Optional
from datetime import date, datetime

class BeefCattleDatabaseSimple:
    def __init__(self):
        pass
        
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Get summary data for dashboard
        """
        return {
            "total_cattle": 5,
            "cattle_by_status": [
                {"status": "Em Engorda", "count": 4},
                {"status": "Vendido", "count": 1}
            ],
            "average_weight": 460.0,
            "monthly_sales": 11700.00
        }
        
    def get_all_beef_cattle(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Get all beef cattle records with optional filters
        """
        return [
            {
                "id": 1,
                "official_id": "BG001",
                "name": "Sultão",
                "birth_date": "2023-01-15",
                "breed": "Nelore",
                "gender": "M",
                "entry_date": "2024-01-10",
                "entry_weight": 380.5,
                "current_weight": 450.2,
                "target_weight": 550.0,
                "status": "Em Engorda",
                "expected_finish_date": "2024-12-15",
                "notes": "Animal saudável, boa conversão alimentar",
                "created_at": "2024-01-10T00:00:00",
                "updated_at": "2024-04-10T00:00:00"
            },
            {
                "id": 2,
                "official_id": "BG002",
                "name": "Trovão",
                "birth_date": "2023-02-20",
                "breed": "Angus",
                "gender": "M",
                "entry_date": "2024-01-15",
                "entry_weight": 410.0,
                "current_weight": 470.5,
                "target_weight": 580.0,
                "status": "Em Engorda",
                "expected_finish_date": "2024-11-20",
                "notes": "Cruzamento industrial, alto ganho diário",
                "created_at": "2024-01-15T00:00:00",
                "updated_at": "2024-04-15T00:00:00"
            }
        ]
        
    def get_sale_records(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get sale records with filters
        """
        return [
            {
                "id": 1,
                "cattle_id": 5,
                "official_id": "BG005",
                "name": "Relâmpago",
                "sale_date": "2024-03-20",
                "final_weight": 520.0,
                "price_per_kg": 22.50,
                "total_value": 11700.00,
                "buyer": "Frigorífico São José",
                "notes": "Venda antecipada por bom desempenho",
                "user_id": 1,
                "created_at": "2024-03-20T00:00:00"
            }
        ]
        
    def get_weight_gain_data(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get weight gain data for dashboard
        """
        return [
            {
                "id": 1,
                "official_id": "BG001",
                "name": "Sultão",
                "first_date": "2024-01-10",
                "last_date": "2024-04-10",
                "initial_weight": 380.5,
                "current_weight": 450.2,
                "days": 90,
                "weight_gain": 69.7,
                "daily_gain": 0.77
            },
            {
                "id": 2,
                "official_id": "BG002",
                "name": "Trovão",
                "first_date": "2024-01-15",
                "last_date": "2024-04-15",
                "initial_weight": 410.0,
                "current_weight": 470.5,
                "days": 90,
                "weight_gain": 60.5,
                "daily_gain": 0.67
            }
        ]

# Create an instance of the database class
beef_cattle_db_simple = BeefCattleDatabaseSimple()