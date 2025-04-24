# REFilterLeads

This project provides two different implementations for lead verification:

## Directory Structure

```
REFilterLeads/
├── free_api/              # Free API Implementation
│   ├── free_lead_verification.py
│   ├── test_numverify.py
│   ├── test_free_verification.py
│   ├── sample_leads.csv
│   └── sample.env
│
└── forewarn/             # Forewarn API Implementation
    ├── lead_verification.py
    ├── lead_utils.py
    ├── mock_forewarn_api.py
    ├── test_lead_verification.py
    └── Project Guide for Forewarn API Integration.markdown
```

## Free API Implementation

Located in the `free_api` directory, this implementation uses free APIs for lead verification:
- Numverify for phone verification
- NeverBounce for email verification
- Searchbug for background checks

### Setup
1. Copy `sample.env` to `.env` and add your API keys
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: 
   - `python test_numverify.py` for API testing
   - `python test_free_verification.py` for unit tests

## Forewarn Implementation

Located in the `forewarn` directory, this implementation uses the Forewarn API for comprehensive lead verification.

### Setup
1. Follow the instructions in the Project Guide
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python test_lead_verification.py`

## Requirements

Both implementations require:
- Python 3.6+
- requests
- python-dotenv
- pytest (for testing)

Install all requirements:
```bash
pip install -r requirements.txt
```

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

# Lead Verification System

A web-based lead verification system with a TypeScript frontend and Python backend.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Build the TypeScript frontend:
```bash
npm run build
```

4. Run the Flask application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`.

## Development

- Frontend TypeScript files are in the `src` directory
- Compiled JavaScript files are output to `dist` directory
- Static files (HTML, JS) are served from the `static` directory
- Python backend code is in the root directory

To watch for TypeScript changes during development:
```bash
npm run watch
```

## Project Structure

```
.
├── src/                    # TypeScript source files
│   ├── main.ts            # Main application logic
│   ├── types.ts           # TypeScript type definitions
│   └── index.html         # Main HTML template
├── static/                # Static files served by Flask
│   ├── js/               # Compiled JavaScript
│   └── index.html        # Copied from src/
├── dist/                  # TypeScript compilation output
├── app.py                # Flask application
├── requirements.txt      # Python dependencies
├── package.json         # Node.js dependencies
└── tsconfig.json        # TypeScript configuration
``` 