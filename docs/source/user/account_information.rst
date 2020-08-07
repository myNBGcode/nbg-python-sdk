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

The Account Information API utilizes OAuth2 for authentication. The OAuth2 authentication flow can be described in a few steps:


1. Prompt user to visit the URL from
   :meth:`get_authorization_code_url() <nbg.account_information.AccountInformationPSD2Client.get_authorization_code_url>`.
2. After they authenticate with their NBG account, they will be redirected to the ``redirect_url`` you provided
3. Grab the ``authorization_code`` from the ``code`` GET parameters in the ``redirect_url``
4. Exchange the ``authorization_code`` for an ``access_token`` with
   :meth:`set_access_token_from_authorization_code() <nbg.account_information.AccountInformationPSD2Client.set_access_token_from_authorization_code>`.

.. code-block:: python

    from nbg.account_information import AccountInformationPSD2Client

    client = AccountInformationPSD2Client(
        client_id="your_app_client_id",
        client_secret="your_app_client_secret",
    )

    # Let's assume that this code runs in a Django view, where the
    # `request` object is available.
    authorization_code = request.GET["code"]
    client.set_access_token_from_authorization_code(authorization_code)

    accounts = client.accounts(user_id="your_user_id")

Authentication API reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: nbg.account_information.AccountInformationPSD2Client.get_authorization_code_url
.. automethod:: nbg.account_information.AccountInformationPSD2Client.set_access_token_from_authorization_code
.. automethod:: nbg.account_information.AccountInformationPSD2Client.set_access_token

Consents
--------

The Account Information API utilizes the concept of concerns to ensure that API actions are authorized by the user at any given time. You can utilize the consent flow, after completing successfully the authentication flow described above. The consent flow can be described in a few steps:

1. Generate a consent via
   :meth:`generate_consent() <nbg.account_information.AccountInformationPSD2Client.generate_consent>`.
2. Store the consent ID for the current client session via
   :meth:`set_consent_id() <nbg.account_information.AccountInformationPSD2Client.set_consent_id>`.
3. Prompt user to provide their consent by visiting the URL from
   :meth:`get_user_consent_url() <nbg.account_information.AccountInformationPSD2Client.get_user_consent_url>`.

.. code-block:: python

    from nbg.account_information import AccountInformationPSD2Client

    client = AccountInformationPSD2Client(
        client_id="your_app_client_id",
        client_secret="your_app_client_secret",
    )

    # Complete authentication flow successfully first.

    consent = client.generate_consent()
    client.set_consent_id(consent["consentId"])

    # Navigate the user to the following URL to get their consent
    consent_url = client.get_user_consent_url(
        redirect_url="https://myapp.example.com/nbg/consent/"
    )

Consents API reference
^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: nbg.account_information.AccountInformationPSD2Client.generate_consent
.. automethod:: nbg.account_information.AccountInformationPSD2Client.set_consent_id
.. automethod:: nbg.account_information.AccountInformationPSD2Client.get_user_consent_url
.. automethod:: nbg.account_information.AccountInformationPSD2Client.get_consent_information
.. automethod:: nbg.account_information.AccountInformationPSD2Client.delete_consent

Sandbox mode
------------

The :class:`AccountInformationPSD2Client <nbg.account_information.AccountInformationPSD2Client>` runs in sandbox mode by default,
and it should do so, unless it's running on a live production environment. In a typical sandbox scenario, you would:

1. Create a unique sandbox, in case you don't have one created already
2. Set the ``sandbox_id`` for your client
3. Use :class:`AccountInformationPSD2Client <nbg.account_information.AccountInformationPSD2Client>`

.. code-block:: python

    from nbg.account_information import AccountInformationPSD2Client

    client = AccountInformationPSD2Client(
        client_id="your_app_client_id",
        client_secret="your_app_client_secret",
    )

    sandbox_id = "your-unique-sandbox-id"
    client.create_sandbox(sandbox_id)
    client.set_sandbox(sandbox_id)

    accounts = client.accounts(user_id="your_user_id")

Sandbox API reference
^^^^^^^^^^^^^^^^^^^^^

.. automethod:: nbg.account_information.AccountInformationPSD2Client.create_sandbox
.. automethod:: nbg.account_information.AccountInformationPSD2Client.export_sandbox
.. automethod:: nbg.account_information.AccountInformationPSD2Client.import_sandbox
.. automethod:: nbg.account_information.AccountInformationPSD2Client.delete_sandbox
.. automethod:: nbg.account_information.AccountInformationPSD2Client.set_sandbox


`AccountInformationPSD2Client`
------------------------------

.. autoclass:: nbg.account_information.AccountInformationPSD2Client
    :members:
