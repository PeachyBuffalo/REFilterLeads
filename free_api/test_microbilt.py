import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
import requests

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from free_lead_verification import LeadVerifier

# Load environment variables
load_dotenv()

class TestMicroBiltIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.verifier = LeadVerifier()
        self.test_name = "John Doe"
        self.test_phone = "+1234567890"
        self.test_email = "john.doe@example.com"

    @patch('requests.post')
    def test_successful_background_check(self, mock_post):
        """Test successful background check with MicroBilt"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
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
            "risk_factors": ["high_risk_address"],
            "criminal_records": [],
            "bankruptcies": []
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Perform background check
        result = self.verifier.check_background(
            self.test_name,
            self.test_phone,
            self.test_email
        )

        # Verify results
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(len(result["addresses"]), 1)
        self.assertEqual(result["risk_factors"], ["high_risk_address"])
        self.assertEqual(result["criminal_records"], [])
        self.assertEqual(result["bankruptcies"], [])

    @patch('requests.post')
    def test_background_check_with_criminal_records(self, mock_post):
        """Test background check with criminal records"""
        # Mock response with criminal records
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "name": "John Doe",
            "addresses": [],
            "risk_factors": ["criminal_history"],
            "criminal_records": [
                {
                    "offense": "DUI",
                    "date": "2020-01-01",
                    "state": "NY"
                }
            ],
            "bankruptcies": []
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Perform background check
        result = self.verifier.check_background(
            self.test_name,
            self.test_phone,
            self.test_email
        )

        # Verify results
        self.assertEqual(len(result["criminal_records"]), 1)
        self.assertEqual(result["criminal_records"][0]["offense"], "DUI")
        self.assertIn("criminal_history", result["risk_factors"])

    @patch('requests.post')
    def test_background_check_with_bankruptcy(self, mock_post):
        """Test background check with bankruptcy records"""
        # Mock response with bankruptcy
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "name": "John Doe",
            "addresses": [],
            "risk_factors": ["bankruptcy"],
            "criminal_records": [],
            "bankruptcies": [
                {
                    "date": "2019-01-01",
                    "chapter": "7",
                    "state": "NY"
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Perform background check
        result = self.verifier.check_background(
            self.test_name,
            self.test_phone,
            self.test_email
        )

        # Verify results
        self.assertEqual(len(result["bankruptcies"]), 1)
        self.assertEqual(result["bankruptcies"][0]["chapter"], "7")
        self.assertIn("bankruptcy", result["risk_factors"])

    @patch('requests.post')
    def test_background_check_error_handling(self, mock_post):
        """Test error handling in background check"""
        # Mock API error
        mock_post.side_effect = requests.exceptions.RequestException("API Error")

        # Perform background check
        result = self.verifier.check_background(
            self.test_name,
            self.test_phone,
            self.test_email
        )

        # Verify error handling
        self.assertIn("error", result)
        self.assertEqual(result["error"], "API Error")

    def test_missing_api_key(self):
        """Test behavior when MicroBilt API key is missing"""
        # Temporarily remove API key
        original_key = os.environ.get("MICROBILT_API_KEY")
        if "MICROBILT_API_KEY" in os.environ:
            del os.environ["MICROBILT_API_KEY"]

        # Perform background check
        result = self.verifier.check_background(
            self.test_name,
            self.test_phone,
            self.test_email
        )

        # Verify error message
        self.assertIn("error", result)
        self.assertEqual(result["error"], "MicroBilt API key not configured")

        # Restore API key
        if original_key:
            os.environ["MICROBILT_API_KEY"] = original_key

if __name__ == '__main__':
    unittest.main() 