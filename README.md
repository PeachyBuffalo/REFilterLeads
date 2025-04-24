# REFilterLeads - Real Estate Lead Verification System

A system for verifying real estate leads using free APIs (Numverify, NeverBounce, and Searchbug) to validate contact information and perform basic background checks.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with the following content:
   ```
   # API Keys for Lead Verification
   NUMVERIFY_API_KEY=your_numverify_api_key_here
   NEVERBOUNCE_API_KEY=your_neverbounce_api_key_here
   SEARCHBUG_API_KEY=your_searchbug_api_key_here

   # Optional: Set to true to use mock API for testing
   USE_MOCK_API=false

   # Optional: Set the output directory for JSON files
   OUTPUT_DIR=results

   # Optional: Set the log level (DEBUG, INFO, WARNING, ERROR)
   LOG_LEVEL=INFO
   ```

3. Get your API keys:
   - Numverify: https://numverify.com/
   - NeverBounce: https://www.neverbounce.com/
   - Searchbug: https://www.searchbug.com/

## Usage

### Verifying Leads

Run the lead verification script with sample leads:

```python
from free_lead_verification import process_new_leads, save_leads_to_json

# Your leads as (name, phone, email) tuples
leads = [
    ("John Doe", "1234567890", "john.doe@example.com"),
    ("Jane Smith", "9876543210", "jane.smith@example.com")
]

# Process leads
verified, flagged = process_new_leads(leads)

# Save results
save_leads_to_json(verified, flagged)
```

### Running Tests

Run the test suite:

```
python -m pytest test_free_verification.py -v
```

## Features

- Phone number validation using Numverify
- Email verification using NeverBounce
- Basic background checks using Searchbug
- Risk assessment for each lead
- JSON export of verified and flagged leads
- Comprehensive test coverage

## Output Format

The system exports verified and flagged leads to separate JSON files with this structure:

```json
[
  {
    "name": "John Doe",
    "phone": "123-456-7890",
    "email": "john.doe@example.com",
    "verification_details": {
      "phone_verification": { ... },
      "email_verification": { ... },
      "background_check": { ... },
      "verification_status": {
        "overall_status": "verified",
        "risk_factors": []
      }
    }
  }
]
```

## Notes

- Ensure compliance with data privacy regulations (e.g., GDPR, CCPA) when handling personal data
- Monitor API usage to manage costs, especially for APIs with per-call pricing
- Consider implementing rate limiting for API calls
- Keep your API keys secure and never commit them to version control 