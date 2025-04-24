from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime

@dataclass
class Lead:
    """Base lead schema that all integrations must convert to/from"""
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    source: str
    created_at: datetime
    metadata: Dict[str, Any]
    raw_data: Dict[str, Any]  # Original data from source
    
    # Verification results
    verification_status: Optional[Dict[str, Any]] = None
    risk_score: Optional[float] = None
    risk_factors: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert lead to dictionary format"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
            "verification_status": self.verification_status,
            "risk_score": self.risk_score,
            "risk_factors": self.risk_factors
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Lead':
        """Create lead from dictionary format"""
        return cls(
            id=data.get("id", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            source=data.get("source", ""),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            metadata=data.get("metadata", {}),
            raw_data=data.get("raw_data", {}),
            verification_status=data.get("verification_status"),
            risk_score=data.get("risk_score"),
            risk_factors=data.get("risk_factors")
        ) 