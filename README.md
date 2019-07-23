# NBG Python SDK

## Accounts Information PSD2 API

```python
from datetime import datetime

import nbg


# General client set up
nbg_client = nbg.Client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    production=False,
)
nbg_client.set_access_token("access_token_of_your_user")  # Also sets default `user_id`

# Accounts Information PSD2 client and sandboxsetup
ai_psd2_client = nbg_client.accounts_information_psd2
ai_psd2_client.create_sandbox("sandbox_id")
ai_psd2_client.set_default_sandbox("sandbox_id")
ai_psd2_client.set_consent_id("consent_id")

# Interaction with API

# Account
ai_psd2_client.accounts()
ai_psd2_client.account_beneficiaries(iban="GR7701100800000008000133077")
ai_psd2_client.account_details(account="08000133077")
ai_psd2_client.account_transactions(
    account="08000133077",
    date_from=datetime(2019, 7, 1),
    date_to=datetime(2019, 8, 1),
)

# Foreign Currency Account
ai_psd2_client.foreign_currency_accounts()
ai_psd2_client.foreign_currency_account_beneficiaries(
    account="08000133077",
)
ai_psd2_client.foreign_currency_account_details(
    account="08000133077",
)
ai_psd2_client.foreign_currency_account_transactions(
    account="08000133077",
    date_from=datetime(2019, 7, 1),
    date_to=datetime(2019, 8, 1),
)

# Scheduled Payments
ai_psd2_client.scheduled_payments(
    account="08000133077",
    date_from=datetime(2019, 7, 1),
    date_to=datetime(2019, 8, 1),
)

# Standing Orders
ai_psd2_client.standing_orders(
    account="08000133077",
    date_from=datetime(2019, 7, 1),
    date_to=datetime(2019, 8, 1),
)

# Sandbox
ai_psd2_client.create_sandbox("unique_sandbox_id")
sandbox_data = ai_psd2_client.export_sandbox("unique_sandbox_id")
ai_psd2_client.import_sandbox("another_unique_sandbox_id", sandbox_data)
ai_psd2_client.delete_sandbox("unique_sandbox_id")

# User
ai_psd2_client.current_user()
```
