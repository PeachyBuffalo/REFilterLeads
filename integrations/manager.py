from typing import Dict, Type, List, Any
from .adapters.base import BaseAdapter
from .schemas.lead import Lead
from free_lead_verification import verify_lead

class IntegrationManager:
    """Manages lead source integrations and processing"""
    
    def __init__(self):
        self._adapters: Dict[str, BaseAdapter] = {}
    
    def register_adapter(self, adapter: BaseAdapter) -> None:
        """Register a new adapter"""
        source_name = adapter.get_source_name()
        self._adapters[source_name] = adapter
    
    def get_adapter(self, source_name: str) -> BaseAdapter:
        """Get adapter for a specific source"""
        if source_name not in self._adapters:
            raise ValueError(f"No adapter registered for source: {source_name}")
        return self._adapters[source_name]
    
    def process_lead(self, source_name: str, data: Dict[str, Any]) -> Lead:
        """Process a single lead from a specific source"""
        adapter = self.get_adapter(source_name)
        if not adapter.validate_source_data(data):
            raise ValueError(f"Invalid data format for source: {source_name}")
        
        lead = adapter.convert_to_lead(data)
        verification_result = verify_lead(lead.first_name, lead.last_name, lead.phone, lead.email)
        
        # Update lead with verification results
        lead.verification_status = verification_result
        lead.risk_score = verification_result.get("risk_score")
        lead.risk_factors = verification_result.get("risk_factors")
        
        return lead
    
    def process_batch(self, source_name: str, data_list: List[Dict[str, Any]]) -> List[Lead]:
        """Process multiple leads from a specific source"""
        adapter = self.get_adapter(source_name)
        leads = adapter.process_batch(data_list)
        
        # Process each lead through verification
        for lead in leads:
            verification_result = verify_lead(lead.first_name, lead.last_name, lead.phone, lead.email)
            lead.verification_status = verification_result
            lead.risk_score = verification_result.get("risk_score")
            lead.risk_factors = verification_result.get("risk_factors")
        
        return leads
    
    def export_lead(self, source_name: str, lead: Lead) -> Dict[str, Any]:
        """Export a lead back to source format"""
        adapter = self.get_adapter(source_name)
        return adapter.convert_from_lead(lead)
    
    def export_batch(self, source_name: str, leads: List[Lead]) -> List[Dict[str, Any]]:
        """Export multiple leads back to source format"""
        adapter = self.get_adapter(source_name)
        return adapter.export_batch(leads) 