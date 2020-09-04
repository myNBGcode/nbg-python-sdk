# NBG Python SDK

[![Downloads of nbg on PyPI](https://pepy.tech/badge/nbg)](https://pepy.tech/project/nbg) [![nbg is packaged as wheel](https://img.shields.io/pypi/wheel/nbg.svg)](https://pypi.org/project/nbg/) [![Supported Python versions of nbg](https://img.shields.io/pypi/pyversions/nbg.svg)](https://pypi.org/project/nbg/)

The `nbg <https://pypi.org/project/nbg>`_ Python package enables developers to build applications that use the public APIs of the National Bank of Greece.


## Installation

We suggest using a package manager like [Poetry](https://python-poetry.org) or [Pipenv](https://pipenv.pypa.io) to install `nbg`. This guarantees that the intended version of `nbg` will be installed every time, through content hash checks:

```console
poetry add nbg
```

Alternatively you can use Pipenv:

```console
pipenv install nbg
```

In case you cannot use Poetry or Pipenv, you can always install `nbg` with [pip](https://pip.pypa.io/en/stable/):

```console
pip install nbg
```

## API clients

The National Bank of Greece provides a set of multiple APIs. To use each one of these APIs, you should pick the corresponding client from the `nbg` package.

### Accounts Information PSD2 API

```python
from nbg import account_information


# Step 1 - Set up client and authentication
client_id="your_client_id"
client_secret="your_client_secret"
client = account_information.AccountInformationPSD2Client(
    client_id=client_id,
    client_secret=client_secret,
    production=False,
)
client.set_access_token("access_token_of_your_user")

# Step 2 - Set up a sandbox, when in development
sandbox_id = f"{client_id}_sandbox"
client.create_sandbox(sandbox_id)
client.set_sandbox(sandbox_id)

# Step 3 - Start working with the Account information API

## Account resource
accounts = client.accounts(user_id="your_user_id")
print(accounts)
```
