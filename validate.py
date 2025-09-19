import json
from jsonschema import validate as jsvalidate, ValidationError

def validate(repository_metadata):
    # Load the schema
    with open("vcs-standard-schema.json", "r") as schema_file:
        schema = json.load(schema_file)

    # Example repository metadata to validate

    # Validate the data
    try:
        jsvalidate(instance=repository_metadata, schema=schema)
        return True
    except ValidationError as e:
        print("❌ Validation error:", e.message)
        return False
        
