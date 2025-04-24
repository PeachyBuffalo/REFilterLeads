import requests
import os
import json
import time
import csv
import logging
from dotenv import load_dotenv
from free_lead_verification import LeadVerifier
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def verify_lead(verifier: LeadVerifier, name: str, phone: str, email: str) -> Dict:
    """Verify all information for a single lead"""
    results = {
        "name": name,
        "phone": phone,
        "email": email,
        "phone_verification": verifier.verify_phone(phone),
        "email_verification": verifier.verify_email(email),
        "background_check": verifier.check_background(name, phone, email)
    }
    return results

def process_leads_from_csv(file_path: str):
    """Process leads from a CSV file containing name, phone, and email"""
    verifier = LeadVerifier()
    verified_leads = []
    flagged_leads = []
    
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            leads = list(reader)
        
        total_leads = len(leads)
        logger.info(f"Processing {total_leads} leads from {file_path}")
        
        for index, lead in enumerate(leads, 1):
            logger.info(f"\nProcessing lead {index}/{total_leads}: {lead['name']}")
            result = verify_lead(verifier, lead['name'], lead['phone'], lead['email'])
            
            # Print verification results
            print("\nPhone Verification:")
            phone_result = result['phone_verification']
            if phone_result.get('valid'):
                print(f"✅ Valid phone number")
                print(f"Location: {phone_result.get('location', 'Unknown')}")
                print(f"Carrier: {phone_result.get('carrier', 'Unknown')}")
            else:
                print(f"❌ Invalid phone number")
                if 'error' in phone_result:
                    print(f"Error: {phone_result['error']}")
            
            print("\nEmail Verification:")
            email_result = result['email_verification']
            if email_result.get('result') == 'valid':
                print("✅ Valid email address")
            else:
                print("❌ Invalid email address")
                if 'error' in email_result:
                    print(f"Error: {email_result['error']}")
            
            print("\nBackground Check:")
            bg_result = result['background_check']
            if 'error' not in bg_result:
                print("✅ Background check completed")
                # Add more detailed background check results here
            else:
                print(f"❌ Error in background check: {bg_result.get('error')}")
            
            # Add delay to avoid rate limiting
            time.sleep(1)
            
            # Save results
            if all([
                phone_result.get('valid'),
                email_result.get('result') == 'valid',
                'error' not in bg_result
            ]):
                verified_leads.append(result)
            else:
                flagged_leads.append(result)
        
        # Save results to JSON files
        os.makedirs('results', exist_ok=True)
        with open('results/verified_leads.json', 'w') as f:
            json.dump(verified_leads, f, indent=2)
        with open('results/flagged_leads.json', 'w') as f:
            json.dump(flagged_leads, f, indent=2)
        
        logger.info(f"\nVerification complete!")
        logger.info(f"Verified leads: {len(verified_leads)}")
        logger.info(f"Flagged leads: {len(flagged_leads)}")
        logger.info("Results saved to 'results' directory")
            
    except FileNotFoundError:
        logger.error(f"Error: File {file_path} not found")
    except Exception as e:
        logger.error(f"Error processing file: {e}")

if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "sample_leads.csv")
    
    # Process leads from the sample CSV file
    process_leads_from_csv(csv_path) 