from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from free_lead_verification import LeadVerifier

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'success',
            'message': 'REFilterLeads API is running',
            'endpoints': {
                'POST /': 'Verify a lead (requires name, phone, email)'
            }
        }).encode())
        return

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Validate required fields
            required_fields = ['name', 'phone', 'email']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Missing required fields',
                    'missing_fields': missing_fields
                }).encode())
                return
            
            # Verify the lead
            verifier = LeadVerifier()
            result = verifier.verify_lead(
                data['name'],
                data['phone'],
                data['email']
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': 'Invalid JSON in request body'
            }).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e)
            }).encode())
        
        return 