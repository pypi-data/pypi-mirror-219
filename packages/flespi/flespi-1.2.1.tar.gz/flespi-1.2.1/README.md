# Flespi REST API wrapper for Python
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://gitlab.com/goldenm-software/open-source-libraries/flespi-python/blob/master/LICENSE) [![pypi version](https://badge.fury.io/py/flespi.svg)](https://pypi.org/project/flespi/)

## Installation
Use the package manager [pip](https://pypi.org/) to install flespi

```bash
$ pip3 install flespi
```

### Usage
```python
from flespi import FlespiClient
# Or
from flespi.rest import FlespiClient

token = 'your_token' # Without "FlespiToken"
# Initialize Flespi instance
flespi = FlespiClient(token)

response = flespi.get('/gw/devices/all')

print(response)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)