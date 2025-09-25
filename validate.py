import json
from jsonschema import validate as json_schema_validate, ValidationError
from datetime import datetime
from typing import List, Optional

# Load the schema
with open("vcs-standard.schema.json", "r") as schema_file:
    schema = json.load(schema_file)

threshold_date = "2025-01-01"
threshold = datetime.strptime(threshold_date, "%Y-%m-%d")

properties_required_after_threshold = [
    'name',
    'description',
    'contractAwardUrls',
]

def validate(repository_metadata):
    validation_result = ValidationResult(True)
    # Step 1: Validate against JSON Schema
    try:
        json_schema_validate(instance=repository_metadata, schema=schema)
    except ValidationError as e:
        validation_result.add_error(e.message)
        validation_result.is_valid = False     
        return validation_result
    
   # Step 2: Custom logic

   # If lastModified > threshold, description is required
    last_modified = datetime.strptime(repository_metadata["lastModified"], "%Y-%m-%d")
    
    if last_modified > threshold:
        for property in properties_required_after_threshold:
            if None == repository_metadata.get(property):
                validation_result.add_error(f"{property} is required for repositories modified after {threshold_date}.")
                validation_result.is_valid = False
    
    # If visibility="Private", is an exemption URL defined?

    if 'Private' == repository_metadata.get('visibility'):
        if None == repository_metadata.get('exemptionUrl'):
            validation_result.add_error('"exemptionUrl" is required when "visibility" is "Private"')

    return validation_result

class ValidationResult:
    def __init__(self, is_valid: bool, errors: Optional[List[str]] = None):
        self.is_valid = is_valid
        self.errors = errors or []

    def add_error(self, message: str):
        self.errors.append(message)
        self.is_valid = False

    def __str__(self):
        if self.is_valid:
            return "✅ Validation passed with no errors."
        else:
            return f"❌ Validation failed with {len(self.errors)} error(s):\n" + "\n".join(f"- {e}" for e in self.errors)
