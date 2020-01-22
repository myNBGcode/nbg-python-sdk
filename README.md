# NBG Python SDK

Python wrapper with unified developer experience for the APIs of the National Bank of Greece.

## Requirements

- Python 3.6 or newer

## Installation

```shell
pipenv install nbg
```

## API clients

The National Bank of Greece provides a set of multiple APIs. To use each one of these APIs, you should pick the corresponding client from the `nbg` package.

### Accounts Information PSD2 API

```python
from datetime import datetime

import nbg


# Step 1 - Set up client and authentication
client = nbg.AccountInformationPSD2Client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    production=False,
)
client.set_access_token("access_token_of_your_user")  # Also sets default `user_id`

# Step 2 - Set up a sandbox, when in development
client.create_sandbox("sandbox_id")
client.set_sandbox("sandbox_id")

# Step 3 - Start working with the Account information API

## Account resource
client.accounts()
client.account_beneficiaries(iban="GR7701100800000008000133077")
client.account_details(account="08000133077")
client.account_transactions(
    account="08000133077",
    date_from=datetime(2019, 7, 1),
    date_to=datetime(2019, 8, 1),
)

## Foreign Currency Account resource
client.foreign_currency_accounts()
client.foreign_currency_account_beneficiaries(
    account="08000133077",
)
client.foreign_currency_account_details(
    account="08000133077",
)
client.foreign_currency_account_transactions(
    account="08000133077",
    date_from=datetime(2019, 7, 1),
    date_to=datetime(2019, 8, 1),
)

## Scheduled Payments resource
client.scheduled_payments(
    account="08000133077",
    date_from=datetime(2019, 7, 1),
    date_to=datetime(2019, 8, 1),
)

## Standing Orders resource
client.standing_orders(
    account="08000133077",
    date_from=datetime(2019, 7, 1),
    date_to=datetime(2019, 8, 1),
)

## Sandbox resource
client.create_sandbox("unique_sandbox_id")
sandbox_data = client.export_sandbox("unique_sandbox_id")
client.import_sandbox("another_unique_sandbox_id", sandbox_data)
client.delete_sandbox("unique_sandbox_id")

## User resource
client.current_user()
```
