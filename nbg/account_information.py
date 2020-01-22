from datetime import datetime

from .base import client, decorators


class AccountInformationPSD2Client(client.BaseClient):
    _production_base_url = "https://services.nbg.gr/apis/account.info/v2"
    _sandbox_base_url = "https://apis.nbg.gr/sandbox/account.info/oauth2/v2"

    _production_scopes = [
        "openid",
        "profile",
        "ibank_profile",
        "role",
        "sandbox-account-info-api-v2",
    ]
    _sandbox_scopes = ["openid", "profile", "role", "sandbox-account-info-api-v2"]

    def accounts(self, userId: str) -> dict:
        """
        [Extensive documentation]
        """
        data = {"userId": userId}
        return self._api_request("POST", "account/list", data)

    def account_beneficiaries(self, iban: str) -> dict:
        """
        [Extensive documentation]
        """
        data = {"iban": iban}
        return self._api_request("POST", "account/beneficiaries", data)

    def account_details(self, account: str) -> dict:
        """
        [Extensive documentation]
        """
        data = {"account": account}
        return self._api_request("POST", "account/details", data)

    def account_transactions(
        self, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        [Extensive documentation]
        """
        data = {"account": account, "dateFrom": date_from, "dateTo": date_to}
        return self._api_request("POST", "account/transactions", data)

    def foreign_currency_accounts(self) -> dict:
        """
        [Extensive documentation]
        """
        return self._api_request("POST", "foreign-currency-account/list")

    def foreign_currency_account_beneficiaries(self, account: str) -> dict:
        """
        [Extensive documentation]
        """
        data = {"account": account}
        return self._api_request("POST", "foreign-currency-account/beneficiaries", data)

    def foreign_currency_account_details(self, account: str) -> dict:
        """
        [Extensive documentation]
        """
        data = {"account": account}
        return self._api_request("POST", "foreign-currency-account/details", data)

    def foreign_currency_account_transactions(
        self, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        [Extensive documentation]
        """
        data = {"account": account, "dateFrom": date_from, "dateTo": date_to}
        return self._api_request("POST", "foreign-currency-account/transactions", data)

    def scheduled_payments(
        self, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        Get scheduled payments. [Extensive documentation]
        """
        data = {"account": account, "dateFrom": date_from, "dateTo": date_to}
        return self._api_request("POST", "scheduled-payments/list", data)

    def standing_orders(
        self, account: str, date_from: datetime, date_to: datetime
    ) -> dict:
        """
        Retrieves standing orders list for a specified account. [Extensive documentation]
        """
        data = {"account": account, "dateFrom": date_from, "dateTo": date_to}
        return self._api_request("POST", "standing-orders/list", data)
