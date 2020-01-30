Guides
======

Getting started
---------------

.. code-block:: python

    from nbg.account_information import AccountInformationPSD2Client

    client = AccountInformationPSD2Client(
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
