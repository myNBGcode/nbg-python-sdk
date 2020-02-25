# NBG Python SDK

Python wrapper with unified developer experience for the APIs of the National Bank of Greece.

## Requirements

- Python 3.6 or newer

## Installation

```shell
poetry add nbg
```

## API clients

The National Bank of Greece provides a set of multiple APIs. To use each one of these APIs, you should pick the corresponding client from the `nbg` package.

### Accounts Information PSD2 API

```python
from nbg.account_information import AccountInformationPSD2Client


# Step 1 - Set up client and authentication
client = nbg.AccountInformationPSD2Client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    production=False,
)
client.set_access_token("access_token_of_your_user")

# Step 2 - Set up a sandbox, when in development
client.create_sandbox("sandbox_id")
client.set_sandbox("sandbox_id")

# Step 3 - Start working with the Account information API

## Account resource
client.accounts("your_user_id")
```
