from datetime import datetime

from .base import client, decorators


class AccountInformationPSD2Client(client.BaseClient):
    _production_base_url = "https://services.nbg.gr/apis/account.info/v2.1"
    _sandbox_base_url = "https://apis.nbg.gr/sandbox/account.info/oauth2/v2.1"

    _production_scopes = [
        "openid",
        "profile",
        "ibank_profile",
        "role",
        "account-info-api-v2-1",
    ]
    _sandbox_scopes = ["openid", "profile", "role", "sandbox-account-info-api-v2-1"]

    def accounts(self, user_id: str) -> dict:
        """
        List domestic accounts in Εuro for the given user.

        :param user_id: The user ID of the corresponding user.
        :type user_id: string
        """
        data = {"userId": user_id}
        return self._api_request("POST", "account/list", data)

    def account_beneficiaries(self, user_id: str, iban: str) -> dict:
        """
        List beneficiaries of a domestic account.

        :param user_id: The user ID of user owning the account.
        :type user_id: string
        :param iban: The IBAN of the domestic account.
        :type iban: string
        """
        data = {"userId": user_id, "iban": iban}
        return self._api_request("POST", "account/beneficiaries", data)

    def account_details(self, user_id: str, account: str) -> dict:
        """
        Retrieve details of a domestic account.

        :param user_id: The user ID of user owning the account.
        :type user_id: string
        :param account: The number of the domestic account.
        :type account: string
        """
        data = {"userId": user_id, "account": account}
        return self._api_request("POST", "account/details", data)

    def account_transactions(
        self, user_id: str, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        List transactions of a domestic account in a given time period.

        :param user_id: The user ID of user owning the account.
        :type user_id: string
        :param account: The number of the domestic account.
        :type account: string
        :param date_from: The datetime after which to look for transactions.
        :type date_from: datetime
        :param date_to: The datetime after which to look for transactions.
        :type date_to: datetime
        """
        data = {
            "userId": user_id,
            "account": account,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        return self._api_request("POST", "account/transactions", data)

    def cards(self, user_id: str) -> dict:
        """
        List of credit and debit cards for the given user.

        :param user_id: The user ID of the corresponding user.
        :type user_id: string
        """
        data = {"userId": user_id}
        return self._api_request("POST", "card/list", data)

    def card_details(self, user_id: str, card_number: str) -> dict:
        """
        Retrieve detailed information for the given credit or debit card.

        :param user_id: The user ID of user owning the account.
        :type user_id: string
        :param card_number: The number of the card.
        :type card_number: string
        """
        data = {"userId": user_id, "cardNumber": card_number}
        return self._api_request("POST", "card/details", data)

    def card_transactions(
        self, user_id: str, card_number: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        List transactions of a credit or debit cart in a given time period.

        :param user_id: The user ID of user owning the account.
        :type user_id: string
        :param card_number: The number of the card.
        :type card_number: string
        :param date_from: The datetime after which to look for transactions.
        :type date_from: datetime
        :param date_to: The datetime after which to look for transactions.
        :type date_to: datetime
        """
        data = {
            "userId": user_id,
            "cardNumber": card_number,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        return self._api_request("POST", "card/transactions", data)

    def foreign_currency_accounts(self, user_id: str) -> dict:
        """
        List accounts in foreign currencies (e.g. USD) for the given user.

        :param user_id: The user ID of the corresponding user.
        :type user_id: string
        """
        data = {"userId": user_id}
        return self._api_request("POST", "foreign-currency-account/list", data)

    def foreign_currency_account_beneficiaries(
        self, user_id: str, account: str
    ) -> dict:
        """
        List beneficiaries of a foreign currency account.

        :param user_id: The user ID of the corresponding user.
        :type user_id: string
        :param account: The number of the foreign currency account.
        :type account: string
        """
        data = {"userId": user_id, "account": account}
        return self._api_request("POST", "foreign-currency-account/beneficiaries", data)

    def foreign_currency_account_details(self, user_id: str, account: str) -> dict:
        """
        Retrieve details of a foreign currency account.

        :param user_id: The user ID of user owning the account.
        :type user_id: string
        :param account: The number of the foreign currency account.
        :type account: string
        """
        data = {"userId": user_id, "account": account}
        return self._api_request("POST", "foreign-currency-account/details", data)

    def foreign_currency_account_transactions(
        self, user_id: str, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        List transactions of a foreign currency account in a given time period.

        :param user_id: The user ID of user owning the account.
        :type user_id: string
        :param account: The number of the foreign currency account.
        :type account: string
        :param date_from: The datetime after which to look for transactions.
        :type date_from: datetime
        :param date_to: The datetime after which to look for transactions.
        :type date_to: datetime
        """
        data = {
            "userId": user_id,
            "account": account,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        return self._api_request("POST", "foreign-currency-account/transactions", data)

    def scheduled_payments(
        self, user_id: str, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        List scheduled payments of a domestic account in a given time period.

        :param user_id: The user ID of user owning the account.
        :type user_id: string
        :param account: The number of the domestic account.
        :type account: string
        :param date_from: The datetime after which to look for scheduled payments.
        :type date_from: datetime
        :param date_to: The datetime until which to look for scheduled payments.
        :type date_to: datetime
        """
        data = {
            "userId": user_id,
            "account": account,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        return self._api_request("POST", "scheduled-payments/list", data)

    def standing_orders(
        self, user_id: str, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        List standing orders of a domestic account in a given time period.

        :param user_id: The user ID of user owning the account.
        :type user_id: string
        :param account: The number of the domestic account.
        :type account: string
        :param date_from: The datetime after which to look for standing orders.
        :type date_from: datetime
        :param date_to: The datetime until which to look for standing orders.
        :type date_to: datetime
        """
        data = {
            "userId": user_id,
            "account": account,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        return self._api_request("POST", "standing-orders/list", data)
