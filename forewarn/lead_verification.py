import requests
import json
import os
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Configuration - will use environment variables if available, otherwise fallback to mock
USE_MOCK_API = os.getenv("USE_MOCK_API", "true").lower() == "true"
API_KEY = os.getenv("FOREWARN_API_KEY", "your_forewarn_api_key")

# API URLs
MOCK_API_URL = "http://localhost:5000/verify"
REAL_API_URL = os.getenv("FOREWARN_API_URL", "https://api.forewarn.com/verify")  # Replace when you get the real URL

def verify_lead(name, phone_number):
    """
    Verify a lead's name and phone number using either the real Forewarn API or mock API.
    Returns True if valid, False if mismatched or fake.
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    # Add authorization header only for the real API
    if not USE_MOCK_API:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    # Payload for the API request
    payload = {
        "name": name,
        "phone_number": phone_number
    }
    
    # Select the appropriate API URL
    api_url = MOCK_API_URL if USE_MOCK_API else REAL_API_URL
    
    try:
        # Send request to API
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the API response
        result = response.json()
        
        # Check if name matches the phone number in API's database
        if result.get("status") == "match":
            return True
        else:
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error verifying lead {name}: {e}")
        return False  # Assume invalid if API fails

def process_new_leads(leads):
    """
    Process a list of new leads and flag invalid ones.
    Leads is a list of tuples: (name, phone_number).
    """
    verified_leads = []
    flagged_leads = []
    
    for name, phone_number in leads:
        if verify_lead(name, phone_number):
            verified_leads.append((name, phone_number))
            print(f"Lead verified: {name} - {phone_number}")
        else:
            flagged_leads.append((name, phone_number))
            print(f"Lead flagged: {name} - {phone_number}")
    
    return verified_leads, flagged_leads

def save_leads_to_json(verified_leads, flagged_leads, output_dir=None, use_date_folder=False):
    """
    Save verified and flagged leads to separate JSON files.
    
    Args:
        verified_leads: List of tuples (name, phone) with verified leads
        flagged_leads: List of tuples (name, phone) with flagged leads
        output_dir: Custom directory to save files (default is current directory)
        use_date_folder: If True, creates a date-based subfolder (YYYY-MM-DD)
    """
    # Convert tuples to dictionaries for better JSON structure
    verified_json = [{"name": name, "phone": phone} for name, phone in verified_leads]
    flagged_json = [{"name": name, "phone": phone} for name, phone in flagged_leads]
    
    # Set default output directory if none specified
    if output_dir is None:
        output_dir = "."
    
    # Create date-based subfolder if requested
    if use_date_folder:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        output_dir = os.path.join(output_dir, f"leads_{today}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Write to JSON files
    verified_path = os.path.join(output_dir, "verified_leads.json")
    flagged_path = os.path.join(output_dir, "flagged_leads.json")
    
    with open(verified_path, "w") as f:
        json.dump(verified_json, f, indent=2)
    
    with open(flagged_path, "w") as f:
        json.dump(flagged_json, f, indent=2)
    
    print(f"\nSaved verified leads to {verified_path}")
    print(f"Saved flagged leads to {flagged_path}")
    
    return verified_path, flagged_path

# Example usage
if __name__ == "__main__":
    # Sample new leads
    new_leads = [
        ("John Doe", "123-456-7890"),      # Should match in mock data
        ("Jane Smith", "555-555-5555"),    # Wrong number for Jane in mock data
        ("Bob Johnson", "555-123-4567"),   # Uses name variation in mock data
        ("Maria Garcia", "333-222-1111"),  # Should match in mock data
        ("Unknown Person", "999-888-7777") # Not in mock database
    ]
    
    # Check which API we're using
    api_mode = "MOCK" if USE_MOCK_API else "REAL"
    print(f"Running in {api_mode} API mode")
    
    # Process the leads
    verified, flagged = process_new_leads(new_leads)
    
    # Output results
    print("\nVerified Leads:", verified)
    print("Flagged Leads:", flagged)
    
    # Save to JSON files
    save_leads_to_json(verified, flagged, use_date_folder=True)