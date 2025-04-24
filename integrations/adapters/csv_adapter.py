from typing import Dict, Any
from .base import BaseAdapter
from ..schemas.lead import Lead
from datetime import datetime

class CSVAdapter(BaseAdapter):
    """Adapter for handling CSV-formatted lead data"""
    
    def convert_to_lead(self, data: Dict[str, Any]) -> Lead:
        """Convert CSV row to Lead format"""
        return Lead(
            id=str(data.get("id", "")),
            first_name=str(data.get("first_name", "")),
            last_name=str(data.get("last_name", "")),
            email=str(data.get("email", "")),
            phone=str(data.get("phone", "")),
            source="csv",
            created_at=datetime.now(),
            metadata={},
            raw_data=data
        )
    
    def convert_from_lead(self, lead: Lead) -> Dict[str, Any]:
        """Convert Lead to CSV row format"""
        return {
            "id": lead.id,
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "email": lead.email,
            "phone": lead.phone,
            "verification_status": lead.verification_status,
            "risk_score": lead.risk_score,
            "risk_factors": lead.risk_factors
        }
    
    def validate_source_data(self, data: Dict[str, Any]) -> bool:
        """Validate CSV row data"""
        required_fields = ["first_name", "last_name", "email", "phone"]
        return all(field in data for field in required_fields)
    
    def get_source_name(self) -> str:
        return "csv" 