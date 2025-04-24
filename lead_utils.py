import csv
import json
import os
import pandas as pd
from lead_verification import process_new_leads, save_leads_to_json

def load_leads_from_csv(csv_file):
    """
    Load leads from a CSV file.
    CSV should have columns for name and phone number.
    
    Args:
        csv_file: Path to CSV file with leads data
        
    Returns:
        A list of tuples (name, phone)
    """
    leads = []
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        # Try to detect name and phone columns
        headers = reader.fieldnames
        name_col = next((col for col in headers if 'name' in col.lower()), headers[0])
        phone_col = next((col for col in headers if 'phone' in col.lower()), headers[1])
        
        for row in reader:
            name = row[name_col].strip()
            phone = row[phone_col].strip()
            
            if name and phone:  # Skip empty entries
                leads.append((name, phone))
    
    return leads

def load_leads_from_excel(excel_file, sheet_name=0):
    """
    Load leads from an Excel file.
    
    Args:
        excel_file: Path to Excel file with leads data
        sheet_name: Sheet name or index (default is first sheet)
        
    Returns:
        A list of tuples (name, phone)
    """
    # Read Excel file
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Try to detect name and phone columns
    headers = df.columns
    name_col = next((col for col in headers if 'name' in str(col).lower()), headers[0])
    phone_col = next((col for col in headers if 'phone' in str(col).lower()), headers[1])
    
    # Convert to list of tuples
    leads = []
    for _, row in df.iterrows():
        name = str(row[name_col]).strip()
        phone = str(row[phone_col]).strip()
        
        if name and phone and name != "nan" and phone != "nan":  # Skip empty entries
            leads.append((name, phone))
    
    return leads

def process_leads_file(input_file, output_dir=None, use_date_folder=True):
    """
    Process leads from a file (CSV or Excel) and save results as JSON.
    
    Args:
        input_file: Path to CSV or Excel file with leads
        output_dir: Directory to save JSON output (optional)
        use_date_folder: Whether to create a date-based folder for output
        
    Returns:
        Paths to the saved JSON files
    """
    # Determine file type and load leads
    if input_file.lower().endswith('.csv'):
        leads = load_leads_from_csv(input_file)
    elif input_file.lower().endswith(('.xlsx', '.xls')):
        leads = load_leads_from_excel(input_file)
    else:
        raise ValueError(f"Unsupported file format: {input_file}")
    
    print(f"Loaded {len(leads)} leads from {input_file}")
    
    # Process the leads
    verified, flagged = process_new_leads(leads)
    
    # Generate output directory name based on input file if not specified
    if output_dir is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = f"results_{base_name}"
    
    # Save to JSON
    return save_leads_to_json(verified, flagged, output_dir, use_date_folder)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Process leads from a CSV or Excel file")
    parser.add_argument("input_file", help="Path to CSV or Excel file with leads data")
    parser.add_argument("--output", "-o", help="Output directory for JSON files", default=None)
    parser.add_argument("--no-date-folder", action="store_true", help="Don't create date-based folder")
    
    args = parser.parse_args()
    
    try:
        verified_path, flagged_path = process_leads_file(
            args.input_file, 
            args.output, 
            not args.no_date_folder
        )
        print(f"\nProcessing complete!")
        print(f"Verified leads: {verified_path}")
        print(f"Flagged leads: {flagged_path}")
    except Exception as e:
        print(f"Error: {e}") 