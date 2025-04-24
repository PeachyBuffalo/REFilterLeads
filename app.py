from flask import Flask, render_template, request, jsonify
from free_lead_verification import verify_lead
from datetime import datetime
import json
import os

app = Flask(__name__)

# In-memory storage for verifications (replace with database in production)
verifications = []

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/api/verify', methods=['POST'])
def api_verify():
    data = request.json
    result = verify_lead(data['first_name'], data['last_name'], data['phone'], data['email'])
    
    # Store verification result
    verification = {
        'id': len(verifications) + 1,
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email'],
        'phone': data['phone'],
        'status': 'valid' if result['phone_valid'] and result['email_valid'] and result['risk_score'] < 0.5 else 'invalid',
        'risk_score': result['risk_score'],
        'timestamp': datetime.now().isoformat(),
        'details': result
    }
    verifications.append(verification)
    
    return jsonify(result)

@app.route('/api/history')
def api_history():
    search = request.args.get('search', '').lower()
    status = request.args.get('status', '')
    
    filtered = verifications
    
    if search:
        filtered = [v for v in filtered if 
                   search in v['first_name'].lower() or 
                   search in v['last_name'].lower() or 
                   search in v['email'].lower() or 
                   search in v['phone']]
    
    if status:
        filtered = [v for v in filtered if v['status'] == status]
    
    return jsonify({
        'verifications': filtered,
        'total': len(verifications)
    })

@app.route('/api/history/<int:id>')
def api_history_detail(id):
    verification = next((v for v in verifications if v['id'] == id), None)
    if verification:
        return jsonify(verification)
    return jsonify({'error': 'Verification not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 