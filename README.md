# REFilterLeads - Real Estate Lead Verification System

A system for verifying real estate leads by checking if provided phone numbers match the names, using Forewarn API or a mock API for development.

## Features

- Verify leads automatically using name and phone number
- Flag suspicious leads for manual review
- Export verified and flagged leads to separate JSON files
- Import leads from CSV or Excel files
- Supports both a mock API (for development) and the real Forewarn API (for production)
- Easily switch between mock and real API using environment variables

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following content:
   ```
   # Set to "true" to use the mock API, "false" to use the real Forewarn API
   USE_MOCK_API=true

   # Forewarn API credentials (update these when you get real credentials)
   FOREWARN_API_KEY=your_forewarn_api_key
   FOREWARN_API_URL=https://api.forewarn.com/verify
   ```

## Usage

### Running the Mock API Server

Start the mock API server:

```
python mock_forewarn_api.py
```

This will start a local server on port 5000 that mimics the Forewarn API responses.

### Verifying Leads

Run the lead verification script with built-in sample leads:

```
python lead_verification.py
```

The script will process the example leads, print out which ones are verified and which ones are flagged, and export them to JSON files.

### Importing Leads from CSV or Excel

Process leads from a CSV or Excel file:

```
python lead_utils.py sample_leads.csv
```

Options:
- `--output` or `-o`: Specify custom output directory
- `--no-date-folder`: Don't create a date-based folder for output

Example:
```
python lead_utils.py sample_leads.csv --output ./my_results
```

### JSON Export Format

The system exports verified and flagged leads to separate JSON files with this structure:

```json
[
  {
    "name": "John Doe",
    "phone": "123-456-7890"
  },
  {
    "name": "Maria Garcia",
    "phone": "333-222-1111"
  }
]
```

### Running Tests

Run the test suite:

```
pytest test_lead_verification.py
```

## Switching to the Real API

When you receive the real Forewarn API credentials:

1. Update the `.env` file:
   ```
   USE_MOCK_API=false
   FOREWARN_API_KEY=your_actual_api_key
   FOREWARN_API_URL=the_actual_api_url
   ```

2. Run the lead verification script as before - it will now use the real API.

## Project Structure

- `lead_verification.py` - Main script for verifying leads
- `mock_forewarn_api.py` - Mock API server for development
- `lead_utils.py` - Utilities for importing leads from CSV/Excel
- `test_lead_verification.py` - Unit tests
- `requirements.txt` - Project dependencies
- `.env` - Environment configuration
- `sample_leads.csv` - Sample CSV file with leads 