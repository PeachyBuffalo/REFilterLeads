import unittest
from unittest.mock import patch, MagicMock
from free_lead_verification import LeadVerifier, process_new_leads

class TestLeadVerification(unittest.TestCase):
    def setUp(self):
        self.verifier = LeadVerifier()
        
    @patch('free_lead_verification.requests.get')
    def test_verify_phone_success(self, mock_get):
        # Mock successful phone verification
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "valid": True,
            "number": "1234567890",
            "local_format": "123-456-7890",
            "international_format": "+11234567890",
            "country_prefix": "+1",
            "country_code": "US",
            "country_name": "United States of America",
            "location": "New York",
            "carrier": "Verizon",
            "line_type": "mobile"
        }
        mock_get.return_value = mock_response
        
        result = self.verifier.verify_phone("1234567890")
        self.assertTrue(result["valid"])
        self.assertEqual(result["number"], "1234567890")
        
    @patch('free_lead_verification.requests.post')
    def test_verify_email_success(self, mock_post):
        # Mock successful email verification
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": "valid",
            "flags": ["has_dns", "has_dns_mx"],
            "suggested_correction": "",
            "retry_token": "",
            "execution_time": 0.123
        }
        mock_post.return_value = mock_response
        
        result = self.verifier.verify_email("test@example.com")
        self.assertEqual(result["result"], "valid")
        
    @patch('free_lead_verification.requests.get')
    def test_check_background_success(self, mock_get):
        # Mock successful background check
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "name": "John Doe",
            "age": 35,
            "addresses": ["123 Main St, New York, NY"],
            "criminal_records": [],
            "bankruptcies": []
        }
        mock_get.return_value = mock_response
        
        result = self.verifier.check_background("John Doe", "1234567890", "john@example.com")
        self.assertIn("name", result)
        self.assertEqual(result["name"], "John Doe")
        
    def test_process_new_leads(self):
        # Test lead processing with mock verifier
        test_leads = [
            ("John Doe", "1234567890", "john@example.com"),
            ("Invalid Lead", "0000000000", "invalid@email")
        ]
        
        with patch('free_lead_verification.LeadVerifier') as mock_verifier:
            mock_instance = mock_verifier.return_value
            mock_instance.verify_lead.side_effect = [
                {
                    "verification_status": {
                        "overall_status": "verified",
                        "risk_factors": []
                    }
                },
                {
                    "verification_status": {
                        "overall_status": "flagged",
                        "risk_factors": ["invalid_phone", "invalid_email"]
                    }
                }
            ]
            
            verified, flagged = process_new_leads(test_leads)
            
            self.assertEqual(len(verified), 1)
            self.assertEqual(len(flagged), 1)
            self.assertEqual(verified[0]["name"], "John Doe")
            self.assertEqual(flagged[0]["name"], "Invalid Lead")

if __name__ == '__main__':
    unittest.main() 