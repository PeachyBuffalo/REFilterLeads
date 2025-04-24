from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..schemas.lead import Lead

class BaseAdapter(ABC):
    """Base adapter interface for all CRM and lead source integrations"""
    
    @abstractmethod
    def convert_to_lead(self, data: Dict[str, Any]) -> Lead:
        """Convert source-specific data to standard Lead format"""
        pass
    
    @abstractmethod
    def convert_from_lead(self, lead: Lead) -> Dict[str, Any]:
        """Convert standard Lead format to source-specific format"""
        pass
    
    @abstractmethod
    def validate_source_data(self, data: Dict[str, Any]) -> bool:
        """Validate that the incoming data matches the expected format"""
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of the source this adapter handles"""
        pass
    
    def process_batch(self, data_list: List[Dict[str, Any]]) -> List[Lead]:
        """Process a batch of leads from the source"""
        return [self.convert_to_lead(data) for data in data_list]
    
    def export_batch(self, leads: List[Lead]) -> List[Dict[str, Any]]:
        """Export a batch of leads back to the source format"""
        return [self.convert_from_lead(lead) for lead in leads] 