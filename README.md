# OCIO VCS Standards

This repository helps the DOI to fulfill version control system (VCS) standards in support of the draft DOI Open Source Policy and the SHARE IT Act.

* [vcs-standard.schema.json](./vcs-standard.schema.json) describes each field and defines low-level validation constraints
* [validate.py](./validate.py) executes the low-level JSON Schema Validation and provides higher-level semantic validation
* [test.py](./test.py) exercises `validate` on some examples.