import unittest
import json
from validate import validate, ValidationResult
from typing import List, Optional

class TestRepositoryMetadata(unittest.TestCase):
    def assertValid(self, validationResult: ValidationResult):
        return self.assertTrue(validationResult.is_valid, str(validationResult))
    
    def assertInvalid(self, validationResult: ValidationResult):
        return self.assertFalse(validationResult.is_valid, str(validationResult))
    
    def test_valid_federal_repo(self):
        data = {
            "name": "Example Repo",
            "description": "Repository for DOI example code.",
            "lastModified": "2025-09-01",
            "visibility": "Federal",
            "url": "https://code.doi.gov/example-repo",
            "contractAwardUrls": [
                "https://www.usaspending.gov/award/EXAMPLE123"
            ],
            "feedbackMechanism": "Submit issues via GitHub",
            "pointOfContact": "contact@example.gov"
        }
        self.assertValid(validate(data))

    def test_missing_required_field(self):
        data = {
            "name": "Incomplete Repo",
            "visibility": "Public",
            "url": "https://code.doi.gov/incomplete-repo"
            # Missing 'lastModified'
        }
        self.assertInvalid(validate(data))

    def test_valid_public_repo_with_empty_awards(self):
        data = {
            "name": "Public Repo",
            "description": "Public repository with no contracts",
            "lastModified": "2025-08-15",
            "visibility": "Public",
            "url": "https://code.doi.gov/public-repo",
            "contractAwardUrls": [],
            "pointOfContact": "public@example.gov"
        }
        self.assertValid(validate(data))

    def test_invalid_missing_exemption_url_on_private_repo(self):
        data = {
            "name": "Example Repo",
            "description": "Repository for DOI example code.",
            "lastModified": "2025-09-01",
            "visibility": "Private",
            "url": "https://code.doi.gov/example-repo",
            "contractAwardUrls": [
                "https://www.usaspending.gov/award/EXAMPLE123"
            ],
            "feedbackMechanism": "Submit issues via GitHub",
        }
        self.assertInvalid(validate(data))

    def test_valid_populated_exemption_url_on_private_repo(self):
        data = {
            "name": "Example Repo",
            "description": "Repository for DOI example code.",
            "lastModified": "2025-09-01",
            "visibility": "Private",
            "url": "https://code.doi.gov/example-repo",
            "contractAwardUrls": [
                "https://www.usaspending.gov/award/EXAMPLE123"
            ],
            "exemptionUrl": "https://doi.gov/developer/share-it-act-exemptions/example-exemption"
        }
        self.assertValid(validate(data))

if __name__ == "__main__":
    unittest.main()
