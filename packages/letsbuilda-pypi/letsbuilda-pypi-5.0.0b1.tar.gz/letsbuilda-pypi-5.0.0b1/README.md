# letsbuilda-pypi

A wrapper for [PyPI's API and RSS feeds](https://warehouse.pypa.io/api-reference/index.html).

## Usage

### Sync client

```py
from requests import Session
from letsbuilda.pypi import PyPIServices

http_session = Session()
pypi_client = PyPIServices(http_session)

package_metadata = pypi_client.get_package_metadata("letsbuilda-pypi")
```

### Async client

```py
from aiohttp import ClientSession
from letsbuilda.pypi.clients.async_client import PyPIServices

http_session = aiohttp.ClientSession()
pypi_client = PyPIServices(http_session)

package_metadata = await pypi_client.get_package_metadata("letsbuilda-pypi")
```
