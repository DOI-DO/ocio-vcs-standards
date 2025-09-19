import unittest
import json
from validate import validate



class TestRepositoryMetadata(unittest.TestCase):

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
        self.assertTrue(validate(data))

    def test_missing_required_field(self):
        data = {
            "name": "Incomplete Repo",
            "visibility": "Public",
            "url": "https://code.doi.gov/incomplete-repo"
            # Missing 'lastModified'
        }
        self.assertFalse(validate(data))

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
        self.assertTrue(validate(data))

if __name__ == "__main__":
    unittest.main()
