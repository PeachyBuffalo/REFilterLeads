# Free Lead Verification API

This API provides lead verification services using three free APIs:
- Numverify for phone number verification
- NeverBounce for email verification
- MicroBilt for background checks

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```env
NUMVERIFY_API_KEY=your_numverify_key
NEVERBOUNCE_API_KEY=your_neverbounce_key
MICROBILT_API_KEY=your_microbilt_key
```

## API Endpoints

### POST /verify

Verify a lead's information including phone, email, and background check.

**Request Body:**
```json
{
    "name": "John Doe",
    "phone": "+1234567890",
    "email": "john.doe@example.com"
}
```

**Response:**
```json
{
    "phone_verification": {
        "valid": true,
        "number": "+1234567890",
        "local_format": "234567890",
        "international_format": "+1234567890",
        "country_prefix": "+1",
        "country_code": "US",
        "country_name": "United States of America",
        "location": "New York",
        "carrier": "Verizon",
        "line_type": "mobile"
    },
    "email_verification": {
        "result": "valid",
        "flags": ["has_dns", "has_dns_mx"],
        "suggested_correction": "",
        "retry_token": "",
        "execution_time": 0.12
    },
    "background_check": {
        "name": "John Doe",
        "addresses": [
            {
                "address": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "years_lived": 5
            }
        ],
        "risk_factors": ["high_risk_address", "recent_move"],
        "criminal_records": [],
        "bankruptcies": []
    },
    "verification_status": {
        "overall_status": "verified",
        "risk_factors": []
    }
}
```

## Error Responses

The API may return the following error responses:

1. Missing API Keys:
```json
{
    "error": "API key not configured",
    "service": "numverify|neverbounce|microbilt"
}
```

2. Invalid Request:
```json
{
    "error": "Missing required fields",
    "details": ["name", "phone", "email"]
}
```

3. API Service Errors:
```json
{
    "error": "Service error message",
    "service": "numverify|neverbounce|microbilt"
}
```

## Risk Factors

The API checks for the following risk factors:
- Invalid phone number
- Invalid email address
- Criminal records
- Bankruptcy records
- High-risk addresses
- Recent moves
- Other risk factors identified by MicroBilt

## Usage Example

```python
import requests
import json

url = "https://your-api-url/verify"
data = {
    "name": "John Doe",
    "phone": "+1234567890",
    "email": "john.doe@example.com"
}

response = requests.post(url, json=data)
result = response.json()

if result["verification_status"]["overall_status"] == "verified":
    print("Lead verified successfully")
else:
    print("Lead flagged with risk factors:", result["verification_status"]["risk_factors"])
```

## Rate Limits

- Numverify: 100 requests per month (free tier)
- NeverBounce: 1000 credits per month (free tier)
- MicroBilt: Varies based on subscription

## Notes

- Phone numbers should be in international format (e.g., +1234567890)
- Email addresses should be properly formatted
- Background checks may take longer to process than phone/email verification
- Results are cached for 24 hours to optimize API usage 