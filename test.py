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
            "feedbackMechanism": "Submit issues via GitHub",
            "technicalPointOfContact": "contact@example.gov",
            "repositoryOwner": "repo owner",
            "systems": ["system1", "system2"],
            "dataClassification": "Public",
            "status": "Active",
            "primaryTechnologies": ["python", ".NET"],
            "isDeployedToProduction": False,
            "isSbomAvailable": True,
            "hasCicdPipeline": False,
            "containsPiiOrSensitiveData": True
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
            "technicalPointOfContact": "contact@example.gov",
            "repositoryOwner": "repo owner",
            "systems": ["system1", "system2"],
            "dataClassification": "Public",
            "status": "Active",
            "primaryTechnologies": ["python", ".NET"],
            "isDeployedToProduction": False,
            "isSbomAvailable": True,
            "hasCicdPipeline": False,
            "containsPiiOrSensitiveData": True
        }
        self.assertValid(validate(data))

    def test_invalid_missing_exemption_url_on_private_repo(self):
        data = {
            "name": "Example Repo",
            "description": "Repository for DOI example code.",
            "lastModified": "2025-09-01",
            "visibility": "Private",
            "url": "https://code.doi.gov/example-repo",
            "feedbackMechanism": "Submit issues via GitHub",
        }
        self.assertInvalid(validate(data))

    def test_valid_populated_url_on_private_repo(self):
        data = {
            "name": "Example Repo",
            "description": "Repository for DOI example code.",
            "lastModified": "2025-09-01",
            "visibility": "Private",
            "url": "https://code.doi.gov/example-repo",
            "technicalPointOfContact": "contact@example.gov",
            "repositoryOwner": "repo owner",
            "systems": ["system1", "system2", "system3"],
            "dataClassification": "Internal",
            "status": "Archived",
            "primaryTechnologies": ["Node", "React"],
            "isDeployedToProduction": True,
            "isSbomAvailable": True,
            "hasCicdPipeline": True,
            "containsPiiOrSensitiveData": True
        }
        self.assertValid(validate(data))

    def test_invalid_exemption_url_on_private_repo(self):
        data = {
            "name": "Example Repo",
            "description": "Repository for DOI example code.",
            "lastModified": "2025-09-01",
            "visibility": "Private",
            "url": "https://code.doi.gov/example-repo",
            "exemptionUrl": "https://doi.gov/this-is-not-a-share-it-act-exemption-url"
        }
        self.assertInvalid(validate(data))
        
if __name__ == "__main__":
    unittest.main()
