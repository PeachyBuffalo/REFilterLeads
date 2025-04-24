from http.server import BaseHTTPRequestHandler
import json
from free_lead_verification import LeadVerifier

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        verifier = LeadVerifier()
        result = verifier.verify_lead(
            data.get('name', ''),
            data.get('phone', ''),
            data.get('email', '')
        )
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
        
        return 