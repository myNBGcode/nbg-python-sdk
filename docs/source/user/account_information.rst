Account Information API
=======================

The `nbg.account_information` module provides a Python interface to the NBG Account Information API, which is a PSD2 compliant account information interface exposing details of the requested accounts, balances and transactions.

More information about the NBG Account Information API can be found at https://developer.nbg.gr/apiProduct/Account-Information-PSD2.

Getting started
---------------

Before you get started you need to:

1. Create an NBG developer account at https://developer.nbg.gr/
2. Create an organization at https://developer.nbg.gr/organizations
3. Create an app for your organization
4. Subscribe your application to the Account Information - PSD2 API
5. Note down your Client ID and Client Secret

Authentication
--------------

The Account Information API utilizes OAuth2 for authentication and authorization. The OAuth2 authentication flow
can be described in a few steps:

1. You prompt your user to visit an authorization code url via `get_authorization_code_url`
2. After the user authenticates with their NBG account, they will be redirected to the `redirect_url` you provided
3. Your application should grab the `authorization_code` from the GET parameters of the `redirect_url`
4. Your application should exchange the `authorization_code` for an `access_token` via `set_access_token_from_authorization_code`

.. automethod:: nbg.account_information.AccountInformationPSD2Client.get_authorization_code_url
.. automethod:: nbg.account_information.AccountInformationPSD2Client.set_access_token_from_authorization_code
.. automethod:: nbg.account_information.AccountInformationPSD2Client.set_access_token


`AccountInformationPSD2Client`
------------------------------

.. automodule:: nbg.account_information
    :members:
