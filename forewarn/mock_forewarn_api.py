import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database of known individuals
KNOWN_INDIVIDUALS = {
    "John Doe": "123-456-7890",
    "Jane Smith": "987-654-3210", 
    "Robert Johnson": "555-123-4567",
    "Maria Garcia": "333-222-1111",
    "James Wilson": "444-555-6666",
    "Susan Brown": "777-888-9999",
}

# Some variations of names for the same individuals (to simulate real-world complexity)
NAME_VARIATIONS = {
    "Bob Johnson": "Robert Johnson",
    "Rob Johnson": "Robert Johnson",
    "Johnny Doe": "John Doe",
    "Jon Doe": "John Doe",
}

@app.route('/verify', methods=['POST'])
def verify():
    # Get request data
    data = request.json
    name = data.get('name')
    phone_number = data.get('phone_number')
    
    if not name or not phone_number:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check for name variations
    if name in NAME_VARIATIONS:
        name = NAME_VARIATIONS[name]
    
    # Check if the name and phone match in our database
    if name in KNOWN_INDIVIDUALS and KNOWN_INDIVIDUALS[name] == phone_number:
        result = {
            "status": "match",
            "confidence": random.uniform(0.85, 0.99),
            "details": {
                "name_verified": True,
                "phone_verified": True,
                "address_found": random.choice([True, False]),
                "risk_factors": []
            }
        }
    else:
        # Could be a no match, a fake number, or just not in our database
        # For mock purposes, we'll randomly assign different failure reasons
        failure_type = random.choice(["no_match", "invalid_number", "insufficient_data"])
        
        result = {
            "status": failure_type,
            "confidence": random.uniform(0.5, 0.7),
            "details": {
                "name_verified": False,
                "phone_verified": name not in KNOWN_INDIVIDUALS and random.choice([True, False]),
                "risk_factors": random.sample(["number_mismatch", "disposable_number", "voip_number"], 
                                             k=random.randint(0, 2))
            }
        }
    
    # Simulate occasional API failures
    if random.random() < 0.05:  # 5% chance of error
        return jsonify({"error": "Service temporarily unavailable"}), 503
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 