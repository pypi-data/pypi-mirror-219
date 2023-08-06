# Python Client Library for Dependency Health API

Dependency Health provides data about open-source package health. 
It could be used in a CI/CD pipeline or as an IDE plugin.

## Installation

```bash
pip3 install dependencyhealth
```

## Usage

```python
from dependencyhealth.npm import Client
import json
import os

dh = Client(token=os.getenv("DH_TOKEN"))
health_data = dh.check_package("@angular/core")
print(json.dumps(health_data, indent=2))
```

```json
{
  "age": 7,
  "versions": 711,
  "maintainers": 2,
  "dependencies": 1,
  "health": 95,
  "security": "no known security issues",
  "popularity": "key ecosystem project",
  "maintenance": "healthy",
  "community": "active",
  "name": "@angular/core",
  "updated_at": "2023-07-14T13:37:37.573865Z"
}
```