from free_lead_verification import LeadVerifier
import json
import os

def test_lead_verification():
    # Initialize the verifier
    verifier = LeadVerifier()
    
    # Test with a sample lead
    name = "John Smith"
    phone = "6164036921"
    email = "john.smith@example.com"
    
    print(f"\nVerifying lead: {name}")
    print(f"Phone: {phone}")
    print(f"Email: {email}\n")
    
    # Verify the lead
    result = verifier.verify_lead(name, phone, email)
    
    # Print the results
    print("Verification Results:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_lead_verification() 