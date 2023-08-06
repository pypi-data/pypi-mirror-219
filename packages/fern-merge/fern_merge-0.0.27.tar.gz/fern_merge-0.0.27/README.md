
# Merge Python Library

[![pypi](https://img.shields.io/pypi/v/fern-merge.svg)](https://pypi.python.org/pypi/fern-merge)
[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)

The Merge Python library provides access to the Merge API from Python.

## Documentation

API reference documentation is available [here](https://docs.merge.dev/).

## Installation

```
pip install --upgrade fern-merge
```

## Usage

```python
import merge
from merge.client import Merge

client = Merge(api_key="YOUR_API_KEY")

application = client.ats.applications.create(
  model=merge.ats.ApplicationRequest(candidate="2872ba14-4084-492b-be96-e5eee6fc33ef"),
  remote_user_id='98796',
)

print("Created application!", application)
```

## Categories

This SDK contains both the ATS and HRIS Merge Categories and will eventually contain all categories. Even if you do not plan on using more than one Merge API category right now, the SDK provides upgrade-flexibility in case you find new Merge API categories useful in the future.

Each category is namespaced: 
```python
client = Merge(api_key="YOUR_API_KEY")

client.ats. # APIs specific to the ATS Category

client.hris. # APIs specific to the HRIS Category
```

## Beta status

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning the package version to a specific version in your package.json file. This way, you can install the same version each time without breaking changes unless you are intentionally looking for the latest version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
