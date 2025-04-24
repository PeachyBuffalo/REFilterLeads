import unittest
import json
from unittest.mock import patch, MagicMock
from lead_verification import verify_lead, process_new_leads

class TestLeadVerification(unittest.TestCase):
    
    @patch('lead_verification.requests.post')
    def test_verify_lead_success(self, mock_post):
        # Mock a successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "match",
            "confidence": 0.95,
            "details": {
                "name_verified": True,
                "phone_verified": True,
                "address_found": True,
                "risk_factors": []
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test function
        result = verify_lead("John Doe", "123-456-7890")
        
        # Assertions
        self.assertTrue(result)
        mock_post.assert_called_once()
    
    @patch('lead_verification.requests.post')
    def test_verify_lead_failure(self, mock_post):
        # Mock a failed API response (non-matching lead)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "no_match",
            "confidence": 0.65,
            "details": {
                "name_verified": False,
                "phone_verified": True,
                "risk_factors": ["number_mismatch"]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test function
        result = verify_lead("Jane Smith", "555-555-5555")
        
        # Assertions
        self.assertFalse(result)
        mock_post.assert_called_once()
    
    @patch('lead_verification.requests.post')
    def test_verify_lead_api_error(self, mock_post):
        # Mock an API error
        mock_post.side_effect = Exception("API error")
        
        # Test function
        result = verify_lead("Error Test", "999-999-9999")
        
        # Assertions
        self.assertFalse(result)  # Should return False on API error
        mock_post.assert_called_once()
    
    @patch('lead_verification.verify_lead')
    def test_process_new_leads(self, mock_verify_lead):
        # Set up test data
        test_leads = [
            ("Good Lead", "123-456-7890"),
            ("Bad Lead", "555-555-5555"),
            ("Another Good Lead", "987-654-3210")
        ]
        
        # Mock the verify_lead function to return True for first and third leads
        mock_verify_lead.side_effect = [True, False, True]
        
        # Call the function
        verified, flagged = process_new_leads(test_leads)
        
        # Assertions
        self.assertEqual(len(verified), 2)
        self.assertEqual(len(flagged), 1)
        self.assertIn(("Good Lead", "123-456-7890"), verified)
        self.assertIn(("Another Good Lead", "987-654-3210"), verified)
        self.assertIn(("Bad Lead", "555-555-5555"), flagged)

if __name__ == '__main__':
    unittest.main() 