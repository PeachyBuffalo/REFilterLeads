import requests
import json
import os
import logging
from dotenv import load_dotenv
from typing import Tuple, List, Dict, Optional
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
NUMVERIFY_API_KEY = os.getenv("NUMVERIFY_API_KEY")
NEVERBOUNCE_API_KEY = os.getenv("NEVERBOUNCE_API_KEY")
MICROBILT_API_KEY = os.getenv("MICROBILT_API_KEY")


class LeadVerifier:
    def __init__(self):
        """Initialize the lead verifier with API keys"""
        self.numverify_url = "http://apilayer.net/api/validate"
        self.neverbounce_url = "https://api.neverbounce.com/v4/single/check"
        self.microbilt_url = "https://api.microbilt.com/v1/person/search"
        
        # Verify API keys are set
        if not NUMVERIFY_API_KEY:
            logger.warning("NUMVERIFY_API_KEY not found in environment variables")
        if not NEVERBOUNCE_API_KEY:
            logger.warning("NEVERBOUNCE_API_KEY not found in environment variables")
        if not MICROBILT_API_KEY:
            logger.warning("MICROBILT_API_KEY not found in environment variables")

    def verify_phone(self, phone_number: str) -> Dict:
        """Verify phone number using Numverify API"""
        if not NUMVERIFY_API_KEY:
            return {"valid": False, "error": "Numverify API key not configured"}
            
        # Clean phone number (remove non-numeric characters)
        clean_phone = ''.join(filter(str.isdigit, phone_number))
        
        params = {
            "access_key": NUMVERIFY_API_KEY,
            "number": clean_phone,
            "country_code": "US",
            "format": 1
        }
        
        try:
            response = requests.get(self.numverify_url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                logger.error(f"Numverify API error: {result['error']}")
                return {"valid": False, "error": result["error"]}
                
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Error verifying phone number: {e}")
            return {"valid": False, "error": str(e)}

    def verify_email(self, email: str) -> Dict:
        """Verify email using NeverBounce API"""
        if not NEVERBOUNCE_API_KEY:
            return {"result": "invalid", "error": "NeverBounce API key not configured"}
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {NEVERBOUNCE_API_KEY}"
        }
        
        data = {
            "email": email,
            "address_info": True,
            "credits_info": True
        }
        
        try:
            response = requests.post(self.neverbounce_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error verifying email: {e}")
            return {"result": "invalid", "error": str(e)}

    def check_background(self, name: str, phone: str, email: str) -> Dict:
        """Check background information using MicroBilt API"""
        if not MICROBILT_API_KEY:
            logger.warning("MicroBilt API key not configured")
            return {"error": "MicroBilt API key not configured"}
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MICROBILT_API_KEY}"
        }
        
        data = {
            "name": name,
            "phone": phone,
            "email": email,
            "include_risk_factors": True,
            "include_address_history": True
        }
        
        try:
            response = requests.post(self.microbilt_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            return {
                "name": result.get("name"),
                "addresses": result.get("addresses", []),
                "risk_factors": result.get("risk_factors", []),
                "criminal_records": result.get("criminal_records", []),
                "bankruptcies": result.get("bankruptcies", [])
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking background with MicroBilt: {e}")
            return {"error": str(e)}

    def verify_lead(self, name: str, phone: str, email: str) -> Dict:
        """Verify a lead using all three APIs"""
        results = {
            "phone_verification": self.verify_phone(phone),
            "email_verification": self.verify_email(email),
            "background_check": self.check_background(name, phone, email)
        }
        
        # Determine overall verification status
        phone_valid = results["phone_verification"].get("valid", False)
        email_valid = results["email_verification"].get("result") == "valid"
        
        # Basic risk assessment
        risk_factors = []
        if not phone_valid:
            risk_factors.append("invalid_phone")
        if not email_valid:
            risk_factors.append("invalid_email")
        
        # Add background check results
        if "error" not in results["background_check"]:
            background_data = results["background_check"]
            if background_data.get("criminal_records"):
                risk_factors.append("criminal_records")
            if background_data.get("bankruptcies"):
                risk_factors.append("bankruptcies")
            if background_data.get("risk_factors"):
                risk_factors.extend(background_data["risk_factors"])
        
        results["verification_status"] = {
            "overall_status": "verified" if phone_valid and email_valid and not risk_factors else "flagged",
            "risk_factors": risk_factors
        }
        
        return results

def process_new_leads(leads: List[Tuple[str, str, str]]) -> Tuple[List[Dict], List[Dict]]:
    """
    Process a list of new leads and return verified and flagged leads.
    Each lead is a tuple of (name, phone, email).
    """
    verifier = LeadVerifier()
    verified_leads = []
    flagged_leads = []
    
    for name, phone, email in leads:
        result = verifier.verify_lead(name, phone, email)
        
        if result["verification_status"]["overall_status"] == "verified":
            verified_leads.append({
                "name": name,
                "phone": phone,
                "email": email,
                "verification_details": result
            })
        else:
            flagged_leads.append({
                "name": name,
                "phone": phone,
                "email": email,
                "verification_details": result,
                "risk_factors": result["verification_status"]["risk_factors"]
            })
    
    return verified_leads, flagged_leads

def save_leads_to_json(verified_leads: List[Dict], flagged_leads: List[Dict], output_dir: str = "results") -> None:
    """Save verified and flagged leads to separate JSON files"""
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, "verified_leads.json"), "w") as f:
        json.dump(verified_leads, f, indent=2)
    
    with open(os.path.join(output_dir, "flagged_leads.json"), "w") as f:
        json.dump(flagged_leads, f, indent=2)

if __name__ == "__main__":
    # Example usage
    test_leads = [
        ("John Doe", "1234567890", "john.doe@example.com"),
        ("Jane Smith", "9876543210", "jane.smith@example.com"),
        ("Invalid Lead", "0000000000", "invalid@email")
    ]
    
    verified, flagged = process_new_leads(test_leads)
    save_leads_to_json(verified, flagged)
    
    print(f"Verified leads: {len(verified)}")
    print(f"Flagged leads: {len(flagged)}") 